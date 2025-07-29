import axios from "axios";

const SERVER_URL = import.meta.env.VITE_SERVER_URL;

export const createPodcast = async(podcast_description:any) => {
  try{
    const response = await axios.post(`${SERVER_URL}/agent/podcast?topic=${podcast_description.topic}`, {})
    // console.log(response.data)
    return response.data
  }catch(e){
    console.log(e)
    return null
  }
}

export const fetchPodcasts = async () => {
  try{
    const response = await axios.get(`${SERVER_URL}/podcasts`)
    // console.log(response)
    return response

  }catch(e){
    console.log(e)
    return null
  }
};

export const fetchPodcastById = async (podcastId: String) => {
  try{
    const response = await axios.get(`${SERVER_URL}/podcast/${podcastId}`)
    // console.log(response)
    return response.data

  }catch(e){
    console.log(e)
    return null
  }
};

export const fetchJobs = async () =>{
  try{
    const response = await axios.get(`${SERVER_URL}/jobs`)
    // console.log(response)
    return response.data
  }catch(e){
    console.log(e)
    return null
  }
}