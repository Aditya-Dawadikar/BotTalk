import { useState } from 'react';
import './App.css';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  ListItemIcon,
  Box,
  Typography,
  Divider,
} from "@mui/material";
import LibraryMusicIcon from '@mui/icons-material/LibraryMusic';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import Library from './components/Library';
import PodcastView from './components/PodcastView';

const drawerWidth = 240;

function App() {
  const [activeComponent, setActiveComponent] = useState("library");
  const [selectedPodcast, setSelectedPodcast] = useState<any>(null);

  const handleOpenPodcast = (podcast: any) => {
    setSelectedPodcast(podcast);
    setActiveComponent("podcast");
  };

  const renderContent = () => {
    switch (activeComponent) {
      case "library":
        return <Library onPodcastClick={handleOpenPodcast} />;
      case "podcast":
        return <PodcastView podcast={selectedPodcast} onBack={() => setActiveComponent("library")} />;
      default:
        return <Library onPodcastClick={handleOpenPodcast} />;
    }
  };

  return (
    <Box sx={{
      display: "flex"
    }}>
      {/* Sidebar */}
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
            backgroundColor: "#000",
            color: "#fff",
            borderRight: "1px solid #222",
          },
        }}
      >
        <Box sx={{ p: 3, textAlign: "center" }}>
          <Typography variant="h5" sx={{ fontWeight: "bold", letterSpacing: "1px" }}>
            🎙 BotTalk
          </Typography>
        </Box>

        <Divider sx={{ borderColor: "#333" }} />

        <List>
          <ListItem disablePadding>
            <ListItemButton
              onClick={() => setActiveComponent("library")}
              selected={activeComponent === "library"}
              sx={{
                color: activeComponent === "library" ? "var(--color-accent)" : "#fff",
                "&:hover": {
                  backgroundColor: "#1a1a1a",
                },
              }}
            >
              <ListItemIcon sx={{ color: "inherit" }}>
                <LibraryMusicIcon />
              </ListItemIcon>
              <ListItemText primary="Library" />
            </ListItemButton>
          </ListItem>

          {selectedPodcast && (
            <ListItem disablePadding>
              <ListItemButton
                onClick={() => setActiveComponent("podcast")}
                selected={activeComponent === "podcast"}
                sx={{
                  color: activeComponent === "podcast" ? "var(--color-accent)" : "#fff",
                  "&:hover": {
                    backgroundColor: "#1a1a1a",
                  },
                }}
              >
                <ListItemIcon sx={{ color: "inherit" }}>
                  <ArrowBackIcon />
                </ListItemIcon>
                <ListItemText primary="Now Playing" />
              </ListItemButton>
            </ListItem>
          )}
        </List>
      </Drawer>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          backgroundColor: "#121212",
          minHeight: "100vh",
          color: "#fff",
          animation: "ambientFlow 25s ease-in-out infinite alternate",
          background: "radial-gradient(circle at 40% 50%, var(--color-ambient-start) 0%, var(--color-ambient-end) 90%)",
        }}
      >
        {renderContent()}
      </Box>
    </Box>
  );
}

export default App;
