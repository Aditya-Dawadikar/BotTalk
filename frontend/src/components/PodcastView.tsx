import React, { useState, useRef, useEffect } from "react";
import {
  Box,
  Typography,
  Paper,
  Slider,
  IconButton,
  Stack,
  Card,
  CardMedia
} from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import PauseIcon from "@mui/icons-material/Pause";
import { fetchPodcastById } from '../services/podcastService'
import ContentCopyIcon from '@mui/icons-material/ContentCopy';

export default function PodcastView({ podcast }: any) {

  const [podcastDetails, setPodcastDetails] = useState<any>(null)
  const [audioUrl, setAudioUrl] = useState<any>(null)

  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);

  const togglePlay = () => {
    const audio = audioRef.current;
    if (!audio) return;
    if (isPlaying) {
      audio.pause();
    } else {
      audio.play();
    }
    setIsPlaying(!isPlaying);
  };

  const handleProgressChange = (_: Event, value: number | number[]) => {
    const audio = audioRef.current;
    if (!audio || typeof value !== "number") return;
    audio.currentTime = (value / 100) * duration;
    setProgress(value);
  };

  // Sync progress and duration
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateProgress = () => {
      setProgress((audio.currentTime / audio.duration) * 100 || 0);
    };
    const setAudioDuration = () => {
      setDuration(audio.duration || 0);
    };

    audio.addEventListener("timeupdate", updateProgress);
    audio.addEventListener("loadedmetadata", setAudioDuration);

    return () => {
      audio.removeEventListener("timeupdate", updateProgress);
      audio.removeEventListener("loadedmetadata", setAudioDuration);
    };
  }, []);

  useEffect(() => {
    const getPodcastById = async () => {
      const response = await fetchPodcastById(podcast._id)
      setPodcastDetails(response)
    }

    getPodcastById()

  }, [podcast])

  useEffect(() => {
    if (!podcastDetails) return;

    podcastDetails.file_urls.map((elem: any) => {
      const parts = elem.file.split("/")
      if (parts[parts.length - 1] === "final.wav") {
        setAudioUrl(elem.url)
        return
      }
    })

  }, [podcastDetails])

  return (
    <>
      {
        podcast ? <>
          <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh", backgroundColor: "var(--color-bg-primary)" }}>

            <Box
              sx={{
                position: "relative",
                width: "100%",
                height: "20em",
                overflow: "hidden",
                borderRadius: 0,
              }}
            >
              {/* Cover Image */}
              <img
                src={podcast.cover_url}
                alt={podcast.topic}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                }}
              />

              {/* Dark gradient at bottom */}
              <Box
                sx={{
                  position: "absolute",
                  inset: 0,
                  background: "linear-gradient(to top, rgba(0,0,0,1), rgba(0,0,0,0.7) 50%, transparent 100%)",
                }}
              />

              {/* Title overlay */}
              <Typography
                variant="h3"
                sx={{
                  position: "absolute",
                  bottom: 30,
                  left: 30,
                  color: "white",
                  fontWeight: "bold",
                  zIndex: 1,
                }}
              >
                {podcast.meta_data.topic}
              </Typography>
            </Box>


            {/* Content Section */}
            <Box
              sx={{
                display: "flex",
                flexDirection: "row",
                flexWrap: "wrap",
                gap: "1em",
                m: "1em",
                backgroundColor: "var(--color-bg-primary)",
              }}
            >
              {/* <Box
                sx={{
                  position: "relative",
                  width: "35%",
                  aspectRatio: "1 / 1", // perfect square card
                  borderRadius: "1em",
                  overflow: "hidden",
                }}
              > 
                <img
                  src={podcast.cover_url}
                  alt={podcast.topic}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    display: "block",
                  }}
                />

                <Box
                  sx={{
                    position: "absolute",
                    inset: 0,
                    background: `radial-gradient(circle at center, rgba(0,0,0,0.0) 50%, rgba(0,0,0,0.99) 100%)`,
                    zIndex: 1,
                  }}
                />

                {audioUrl && (
                  <Box
                    sx={{
                      position: "absolute",
                      bottom: "1em",
                      left: "1em",
                      right: "1em",
                      zIndex: 2,
                      display: "flex",
                      alignItems: "center",
                      gap: "1em",
                    }}
                  >
                    <IconButton
                      onClick={togglePlay}
                      sx={{
                        backgroundColor: "var(--color-accent)",
                        color: "black",
                        "&:hover": { backgroundColor: "var(--color-accent-hover)" },
                      }}
                    >
                      {isPlaying ? <PauseIcon /> : <PlayArrowIcon />}
                    </IconButton>

                    <Slider
                      value={progress}
                      onChange={handleProgressChange}
                      sx={{
                        flex: 1,
                        color: "var(--color-accent)",
                      }}
                    />

                    <audio ref={audioRef} src={audioUrl} preload="metadata" />
                  </Box>
                )}
              </Box>
              */}

              <Box
                sx={{
                  position: "relative",
                  width: "35%",
                  aspectRatio: "1 / 1",
                  borderRadius: "1em",
                  overflow: "hidden",
                  "&:hover .vignette": {
                    background: `radial-gradient(circle at center, rgba(0,0,0,0.3) 40%, rgba(0,0,0,0.98) 100%)`,
                  },
                  "&:hover .player": {
                    bottom: "20%",
                  },
                  "&:hover .progress": {
                    opacity: 1,
                    transform: "translateY(0)",
                  },
                }}
              >
                {/* 🎨 Cover image */}
                <img
                  src={podcast.cover_url}
                  alt={podcast.topic}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    display: "block",
                  }}
                />

                {/* 🕶️ Vignette (animated on hover) */}
                <Box
                  className="vignette"
                  sx={{
                    position: "absolute",
                    inset: 0,
                    background: `radial-gradient(circle at center, rgba(0,0,0,0.0) 100%, rgba(0,0,0,0.85) 100%)`,
                    zIndex: 1,
                    transition: "background 0.4s ease",
                  }}
                />

                {/* 🎧 Player */}
                {audioUrl && (
                  <Box
                    className="player"
                    sx={{
                      position: "absolute",
                      bottom: "1em",
                      left: "1em",
                      right: "1em",
                      zIndex: 2,
                      display: "flex",
                      alignItems: "center",
                      gap: "1em",
                      transition: "bottom 0.4s ease",
                    }}
                  >
                    <IconButton
                      onClick={togglePlay}
                      sx={{
                        backgroundColor: "var(--color-accent)",
                        color: "black",
                        "&:hover": { backgroundColor: "var(--color-accent-hover)" },
                      }}
                    >
                      {isPlaying ? <PauseIcon /> : <PlayArrowIcon />}
                    </IconButton>

                    {/* 🎚️ Slider only appears on hover */}
                    <Slider
                      className="progress"
                      value={progress}
                      onChange={handleProgressChange}
                      sx={{
                        flex: 1,
                        color: "var(--color-accent)",
                        opacity: 0,
                        transform: "translateY(10px)",
                        transition: "opacity 0.3s ease, transform 0.3s ease",
                      }}
                    />

                    <audio ref={audioRef} src={audioUrl} preload="metadata" />
                  </Box>
                )}
              </Box>



              {/* 📝 Metadata Panel */}
              <Box
                sx={{
                  flex: "1 1 50%",
                  p: "1.5em",
                  borderRadius: "1em",
                  backgroundColor: "var(--color-bg-card)",
                  color: "var(--color-text-primary)",
                }}
              >
                <Typography variant="h6" sx={{ mb: "0.8em" }}>
                  About This Episode
                </Typography>
                <Typography variant="body2" sx={{ mb: "1.5em" }}>
                  {podcast.meta_data.long_desc}
                </Typography>

                <Typography
                  variant="subtitle1"
                  sx={{ mb: "0.8em", color: "var(--color-text-secondary)" }}
                >
                  Characters:
                </Typography>
                <ul style={{ margin: 0, paddingLeft: "1.5em" }}>
                  <li>{podcast.meta_data.host}</li>
                  <li>{podcast.meta_data.guest}</li>
                </ul>

                <Typography
                  variant="caption"
                  sx={{ display: "block", mt: "1.5em", color: "var(--color-text-secondary)" }}
                >
                  Released on {podcast.job_finished_at}
                </Typography>

                <Typography
                  variant="subtitle1"
                  sx={{ mt: "1.5em", mb: "0.5em", color: "var(--color-text-secondary)" }}
                >
                  Share Podcast
                </Typography>
                <Box
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    backgroundColor: "rgba(255, 255, 255, 0.05)",
                    border: "1px solid var(--color-accent)",
                    borderRadius: "0.5em",
                    px: "1em",
                    py: "0.5em",
                    fontSize: "0.9em",
                    color: "var(--color-text-primary)",
                    justifyContent: "space-between",
                    overflowX: "auto",
                  }}
                >
                  <Typography sx={{ whiteSpace: "nowrap", mr: "0.5em" }}>
                    http://bottalks/podcast/{podcast._id}
                  </Typography>
                  <IconButton size="small" sx={{ color: "var(--color-accent)" }}>
                    <ContentCopyIcon fontSize="small" />
                  </IconButton>
                </Box>
              </Box>
            </Box>


          </Box>
        </> : <></>
      }
    </>
  );
}
