import React, { useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Slider,
  IconButton,
  Stack,
} from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import PauseIcon from "@mui/icons-material/Pause";

export default function PodcastView() {
  const [podcast] = useState({
    title: "The Future of AI",
    description: "A deep conversation between AI and a philosopher on the future of artificial intelligence.",
    audioUrl: "/audio/sample.mp3", // Replace with actual audio path
    coverUrl: "https://via.placeholder.com/800x400?text=Podcast+Cover",
    characters: ["Host AI", "Guest Philosopher"],
    date: "July 25, 2025",
  });

  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);

  const togglePlay = () => setIsPlaying(!isPlaying);

  return (
    <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
      {/* Cover Image */}
      <Box
        sx={{
          position: "relative",
          width: "100%",
          height: "300px",
          backgroundImage: `url(${podcast.coverUrl})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <Box
          sx={{
            position: "absolute",
            inset: 0,
            background: "linear-gradient(to bottom, rgba(0,0,0,0.5), rgba(0,0,0,0.9))",
          }}
        />
        <Typography
          variant="h3"
          sx={{
            position: "absolute",
            bottom: 20,
            left: 20,
            color: "white",
            fontWeight: "bold",
          }}
        >
          {podcast.title}
        </Typography>
      </Box>

      {/* Content Section */}
      <Box sx={{ display: "flex", flex: 1, p: 3, gap: 3, backgroundColor: "var(--color-bg-primary)" }}>
        {/* Audio Player */}
        <Box sx={{ flex: 2 }}>
          <Paper
            sx={{
              p: 3,
              borderRadius: 2,
              backgroundColor: "var(--color-bg-card)",
            }}
          >
            <Typography variant="h6" sx={{ mb: 2, color: "var(--color-text-primary)" }}>
              Now Playing
            </Typography>
            <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
              <IconButton
                onClick={togglePlay}
                sx={{
                  backgroundColor: "var(--color-accent)",
                  "&:hover": { backgroundColor: "var(--color-accent-hover)" },
                }}
              >
                {isPlaying ? <PauseIcon /> : <PlayArrowIcon />}
              </IconButton>
              <Slider
                value={progress}
                onChange={(_, val) => setProgress(val as number)}
                sx={{
                  flex: 1,
                  color: "var(--color-accent)",
                }}
              />
            </Stack>
            <audio id="podcast-audio" src={podcast.audioUrl} hidden />
          </Paper>
        </Box>

        {/* Metadata Panel */}
        <Box
          sx={{
            flex: 1,
            p: 2,
            borderRadius: 2,
            backgroundColor: "var(--color-bg-card)",
            color: "var(--color-text-primary)",
          }}
        >
          <Typography variant="h6" sx={{ mb: 1 }}>
            About This Episode
          </Typography>
          <Typography variant="body2" sx={{ mb: 2 }}>
            {podcast.description}
          </Typography>
          <Typography variant="subtitle2" sx={{ mb: 1, color: "var(--color-text-secondary)" }}>
            Characters:
          </Typography>
          <ul style={{ margin: 0, paddingLeft: "20px" }}>
            {podcast.characters.map((char, i) => (
              <li key={i}>{char}</li>
            ))}
          </ul>
          <Typography variant="caption" sx={{ display: "block", mt: 2, color: "var(--color-text-secondary)" }}>
            Released on {podcast.date}
          </Typography>
        </Box>
      </Box>
    </Box>
  );
}
