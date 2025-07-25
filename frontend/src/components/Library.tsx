import React, { useState, useEffect } from "react";
import {
    Box,
    Button,
    Card,
    CardContent,
    CardMedia,
    Grid,
    LinearProgress,
    Typography,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { fetchPodcastCover } from "../services/unsplashService";
import CreatePodcastForm from "./CreatePodcastForm";

// Sample data for running jobs and podcasts
const runningJobs = [
    { id: 1, title: "AI Ethics Debate", progress: 60 },
    { id: 2, title: "Space Exploration Talk", progress: 25 },
];

const initialPodcasts = [
    {
        id: 1,
        title: "The Future of AI",
        description: "A discussion between an AI and a philosopher.",
        cover: "", // will be filled dynamically
    },
    {
        id: 2,
        title: "Quantum Talk",
        description: "Exploring quantum computing and its challenges.",
        cover: "",
    },
    {
        id: 3,
        title: "The History Lens",
        description: "A deep dive into modern history with AI narrators.",
        cover: "",
    },
];

export default function Library({ onPodcastClick }: { onPodcastClick: (podcast: any) => void }) {
    const [podcasts, setPodcasts] = useState(initialPodcasts);
    const [loadingCovers, setLoadingCovers] = useState(false);

    const [openForm, setOpenForm] = useState(false);

    const handleOpenForm = () => setOpenForm(true);
    const handleCloseForm = () => setOpenForm(false);

    const handleCreatePodcast = (data: {
        title: string;
        description: string;
        characters: string;
        prompt: string;
    }) => {
        console.log("New Podcast Data:", data);
        // You can call API or update state here
    };

    useEffect(() => {
        const fetchCovers = async () => {
            setLoadingCovers(true);
            const updatedPodcasts = await Promise.all(
                podcasts.map(async (podcast) => {
                    const result = await fetchPodcastCover(podcast.title);
                    return {
                        ...podcast,
                        cover: result?.regular || "https://via.placeholder.com/300x200?text=Podcast",
                    };
                })
            );
            setPodcasts(updatedPodcasts);
            setLoadingCovers(false);
        };
        fetchCovers();
    }, []);

    return (
        <Box sx={{ p: 3 }}>
            {/* Header Row */}
            <Box sx={{ display: "flex", justifyContent: "space-between", mb: 3 }}>
                <Typography variant="h5" color="var(--color-text-primary)">
                    Library
                </Typography>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={handleOpenForm}
                    sx={{
                        backgroundColor: "var(--color-accent)",
                        color: "black",
                        fontWeight: "bold",
                        "&:hover": { backgroundColor: "var(--color-accent-hover)" },
                    }}
                >
                    Create Podcast
                </Button>
                {/* Create Podcast Form */}
                <CreatePodcastForm
                    open={openForm}
                    onClose={handleCloseForm}
                    onSubmit={handleCreatePodcast}
                />
            </Box>

            {/* Running Jobs */}
            {runningJobs.length > 0 && (
                <Box sx={{ mb: 4 }}>
                    <Typography
                        variant="h6"
                        color="var(--color-text-primary)"
                        sx={{ mb: 2 }}
                    >
                        Running Jobs
                    </Typography>
                    {runningJobs.map((job) => (
                        <Box
                            key={job.id}
                            sx={{
                                mb: 2,
                                p: 2,
                                backgroundColor: "var(--color-bg-card)",
                                borderRadius: 2,
                            }}
                        >
                            <Typography variant="subtitle1" sx={{ mb: 1 }}>
                                {job.title}
                            </Typography>
                            <LinearProgress
                                variant="determinate"
                                value={job.progress}
                                sx={{
                                    height: 8,
                                    borderRadius: 5,
                                    backgroundColor: "var(--color-progress-bg)",
                                    "& .MuiLinearProgress-bar": {
                                        backgroundColor: "var(--color-progress-fill)",
                                    },
                                }}
                            />
                        </Box>
                    ))}
                </Box>
            )}

            {/* Podcast Library */}
            <Typography
                variant="h6"
                color="var(--color-text-primary)"
                sx={{ mb: 2 }}
            >
                Your Podcasts
            </Typography>
            <Grid container spacing={3}>
                {podcasts.map((podcast) => (
                    <Grid item xs={12} sm={6} md={4} lg={3} key={podcast.id}>
                        <Card
                            onClick={() => onPodcastClick(podcast)}
                            sx={{
                                backgroundColor: "var(--color-bg-card)",
                                color: "var(--color-text-primary)",
                                borderRadius: 2,
                                boxShadow: "var(--shadow-elevation)",
                                "&:hover": { transform: "scale(1.02)", transition: "0.3s" },
                            }}
                        >
                            {loadingCovers ? (
                                <Box
                                    sx={{
                                        height: "160px",
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "center",
                                        backgroundColor: "var(--color-bg-secondary)",
                                    }}
                                >
                                    <Typography>Loading...</Typography>
                                </Box>
                            ) : (
                                <CardMedia
                                    component="img"
                                    height="160"
                                    image={podcast.cover}
                                    alt={podcast.title}
                                />
                            )}
                            <CardContent>
                                <Typography variant="h6">{podcast.title}</Typography>
                                <Typography variant="body2" color="var(--color-text-secondary)">
                                    {podcast.description}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
}
