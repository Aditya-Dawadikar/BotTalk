import React, { useState, useEffect } from "react";
import {
    Box,
    Button,
    Card,
    CardContent,
    CardMedia,
    Grid,
    Stepper,
    Step,
    StepLabel,
    Typography,
    Collapse,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CreatePodcastForm from "./CreatePodcastForm";
import { fetchPodcasts, createPodcast, fetchJobs } from "../services/podcastService";
import { useColor } from "color-thief-react";
import { boostLightness, rgbToHex } from "../services/colorService";


const DEFAULT_HOVER_COLOR = "#033114ff"

export default function Library({ onPodcastClick }: { onPodcastClick: (podcast: any) => void }) {
    // const [hoverColor, setHoverColor] = useState<string | null>(null);
    const [hoverColor, setHoverColor] = useState<string>(DEFAULT_HOVER_COLOR);
    const [podcasts, setPodcasts] = useState<any[]>([]);
    const [openForm, setOpenForm] = useState(false);
    const [runningJobs, setRunningJobs] = useState<any[]>([]);
    const [expanded, setExpanded] = useState<{ [id: string]: boolean }>({});

    const toggleExpand = (id: string) => {
        setExpanded(prev => ({ ...prev, [id]: !prev[id] }));
    };

    const jobStages = [
        { key: "flow_generated", label: "Flow Planned" },
        { key: "raw_script_generated", label: "Script Written" },
        { key: "script_generated", label: "Script Cleaned" },
        { key: "summary_generated", label: "Summary Done" },
        { key: "image_generated", label: "Image Created" },
        { key: "audio_generated", label: "Audio Synthesized" },
    ];

    const handleOpenForm = () => setOpenForm(true);
    const handleCloseForm = () => setOpenForm(false);

    const handleCreatePodcast = (topic: string) => {
        const createPodcastAgent = async () => {
            const res = await createPodcast(topic)
            console.log(res)
        }
        createPodcastAgent()
    };

    const getPodcastList = async () => {
        const res = await fetchPodcasts()
        setPodcasts([...res.data])
    }
    const getPendingJobs = async () => {
        const res = await fetchJobs()
        setRunningJobs([...res])
    }

    useEffect(() => {
        getPodcastList()
        getPendingJobs()
    }, [])

    useEffect(()=>{
        const interval = setInterval(()=>{
            getPendingJobs()
        },10*1000)
        return () => clearInterval(interval)
    },[])

    return (
        <Box
            sx={{
                p: 3,
                minHeight: "100vh",
                transition: "background 0.4s ease",
                background: `radial-gradient(circle at 85% 15%, ${hoverColor}80 10%, transparent 70%)`
            }}
        >
            {/* Header Row */}
            <Box sx={{ display: "flex", justifyContent: "space-between", mb: 3 }}>
                <Typography variant="h3" color="var(--color-text-primary)">
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
                            key={job._id}
                            sx={{
                                mb: 2,
                                backgroundColor: "transparent",
                                borderRadius: 2,
                            }}
                        >
                            {runningJobs.map((job) => {
                                const currentStep = jobStages.findIndex(stage => job[stage.key] !== "yes");
                                const activeStep = currentStep === -1 ? jobStages.length : currentStep;

                                return (
                                    <Box
                                        key={job._id}
                                        sx={{
                                            mb: 2,
                                            p: 2,
                                            backgroundColor: "transparent",
                                            borderRadius: 2,
                                        }}
                                    >
                                        <Typography variant="subtitle1" sx={{ mb: 1 }}>
                                            Job ID: {job._id}
                                        </Typography>
                                        <Stepper activeStep={activeStep}>
                                            {jobStages.map((stage, index) => (
                                                <Step key={stage.key} completed={job[stage.key] === "yes"}>
                                                    <StepLabel
                                                        StepIconProps={{
                                                            sx: {
                                                                color: 'var(--color-accent)', // icon color
                                                                '&.Mui-completed': {
                                                                    color: 'var(--color-success)',
                                                                },
                                                            },
                                                        }}
                                                        sx={{
                                                            '& .MuiStepLabel-label': {
                                                                color: 'var(--color-text-secondary)',
                                                            },
                                                            '& .MuiStepLabel-label.Mui-active': {
                                                                color: 'var(--color-accent)',
                                                            },
                                                            '& .MuiStepLabel-label.Mui-completed': {
                                                                color: 'var(--color-success)',
                                                            },
                                                        }}
                                                    >
                                                        {stage.label}
                                                    </StepLabel>
                                                </Step>
                                            ))}
                                        </Stepper>
                                    </Box>
                                );
                            })}

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
                {podcasts.map(podcast => (
                    <PodcastCard
                        key={podcast._id}
                        podcast={podcast}
                        onPodcastClick={onPodcastClick}
                        setHoverColor={setHoverColor}
                    />
                ))}

            </Grid>
        </Box>
    );
}



function PodcastCard({ podcast, onPodcastClick, setHoverColor }: any) {
    const { data: rgb, loading, error } = useColor(podcast.cover_url, "rgbArray", {
        crossOrigin: "anonymous",
    });

    return (
        <Grid item xs={12} sm={6} md={4} lg={3}>
            <Card
                onMouseEnter={() => {
                    if (!loading && !error && rgb) {
                        const brighter = boostLightness(rgb, 0.25);
                        setHoverColor(rgbToHex(brighter));
                    }
                }}
                onMouseLeave={() => setHoverColor(DEFAULT_HOVER_COLOR)}
                onClick={() => onPodcastClick(podcast)}
                sx={{
                    cursor: "pointer",
                    maxWidth: "25em",
                    height: "30em",
                    backgroundColor: "var(--color-bg-card)",
                    color: "var(--color-text-primary)",
                    borderRadius: 5,
                    boxShadow: "var(--shadow-elevation)",
                    transition: "transform 0.2s ease",
                    "&:hover": { transform: "scale(1.02)" },
                }}
            >
                <CardMedia
                    component="img"
                    height="70%"
                    image={podcast.cover_url}
                    alt={podcast.topic}
                    crossOrigin="anonymous"
                />
                <CardContent>
                    <Typography variant="h6">{podcast.topic}</Typography>
                    <Typography variant="body2" color="var(--color-text-secondary)">
                        {podcast.meta_data.short_desc.slice(0, 80)}{podcast.meta_data.short_desc.length > 100 ? "... Read more" : ""}
                    </Typography>
                </CardContent>
            </Card>
        </Grid>
    );
}
