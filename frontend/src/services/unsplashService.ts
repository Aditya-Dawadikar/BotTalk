import axios from "axios";

const UNSPLASH_ACCESS_KEY = import.meta.env.VITE_UNSPLASH_ACCESS_KEY;
const UNSPLASH_API_BASE = "https://api.unsplash.com";

export const fetchPodcastCover = async (query: string = "podcast") => {
  return {
      full: "",
      regular: "",
      thumb: "",
      alt: "",
      photographer: "",
    };

  // try {
  //   const response = await axios.get(`${UNSPLASH_API_BASE}/photos/random`, {
  //     params: {
  //       query,
  //       orientation: "landscape",
  //       content_filter: "high",
  //     },
  //     headers: {
  //       Authorization: `Client-ID ${UNSPLASH_ACCESS_KEY}`,
  //     },
  //   });

  //   // Extract image URLs (full and small for thumbnails)
  //   return {
  //     full: response.data.urls.full,
  //     regular: response.data.urls.regular,
  //     thumb: response.data.urls.thumb,
  //     alt: response.data.alt_description,
  //     photographer: response.data.user.name,
  //   };
  // } catch (error) {
  //   console.error("Error fetching Unsplash image:", error);
  //   return null;
  // }
};
