import React, { useState } from "react";
import {
    Box,
    Button,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    IconButton,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";

interface CreatePodcastFormProps {
    open: boolean;
    onClose: () => void;
    onSubmit: (data: {
        title: string;
        description: string;
        host_name: string;
        host_personality: string;
        guest_name: string;
        guest_personality: string;
    }) => void;
}

export default function CreatePodcastForm({
    open,
    onClose,
    onSubmit,
}: CreatePodcastFormProps) {
    const [formData, setFormData] = useState({
        title: "",
        description: "",
        host_name: "",
        host_personality: "",
        guest_name: "",
        guest_personality: "",
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = () => {
        onSubmit(formData);
        onClose();
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
            <DialogTitle sx={{ m: 0, p: 2 }}>
                Create New Podcast
                <IconButton
                    aria-label="close"
                    onClick={onClose}
                    sx={{
                        position: "absolute",
                        right: 8,
                        top: 8,
                        color: (theme) => theme.palette.grey[500],
                    }}
                >
                    <CloseIcon />
                </IconButton>
            </DialogTitle>
            <DialogContent dividers>
                <Box component="form" sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
                    <TextField
                        label="Podcast Title"
                        name="title"
                        value={formData.title}
                        onChange={handleChange}
                        fullWidth
                        variant="outlined"
                    />
                    <TextField
                        label="Description"
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        multiline
                        rows={3}
                        fullWidth
                        variant="outlined"
                    />
                    <TextField
                        label="Host Name"
                        name="host_name"
                        value={formData.host_name}
                        onChange={handleChange}
                        fullWidth
                        variant="outlined"
                    />
                    <TextField
                        label="Host Personality"
                        name="host_personality"
                        value={formData.host_personality}
                        onChange={handleChange}
                        fullWidth
                        variant="outlined"
                    />
                    <TextField
                        label="Guest Name"
                        name="guest_name"
                        value={formData.guest_name}
                        onChange={handleChange}
                        fullWidth
                        variant="outlined"
                    />
                    <TextField
                        label="Guest Personality"
                        name="guest_personality"
                        value={formData.guest_personality}
                        onChange={handleChange}
                        fullWidth
                        variant="outlined"
                    />
                </Box>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="inherit">
                    Cancel
                </Button>
                <Button
                    onClick={handleSubmit}
                    variant="contained"
                    sx={{
                        backgroundColor: "var(--color-accent)",
                        color: "black",
                        "&:hover": { backgroundColor: "var(--color-accent-hover)" },
                    }}
                >
                    Create
                </Button>
            </DialogActions>
        </Dialog>
    );
}
