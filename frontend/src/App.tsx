import { useState } from 'react';
import './App.css';
import { Drawer, List, ListItem, ListItemButton, ListItemText, Box, Typography } from "@mui/material";
import Library from './components/Library';
import PodcastView from './components/PodcastView'; // Import PodcastView

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
    <Box sx={{ display: "flex" }}>
      {/* Sidebar */}
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
            backgroundColor: "#000",  // Spotify theme
            color: "#fff",
          },
        }}
      >
        <Box sx={{ p: 2, textAlign: "center" }}>
          <Typography variant="h6" color="primary">
            BotTalk
          </Typography>
        </Box>
        <List>
          <ListItem disablePadding>
            <ListItemButton onClick={() => setActiveComponent("library")}>
              <ListItemText primary="Library" />
            </ListItemButton>
          </ListItem>
        </List>
      </Drawer>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          backgroundColor: "#121212",
          minHeight: "100vh",
          color: "#fff",
        }}
      >
        {renderContent()}
      </Box>
    </Box>
  );
}

export default App;
