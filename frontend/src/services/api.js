import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
});

export const getTags = async () => {
  const response = await api.get('/tags');
  return response.data.tags;
};

export const getModels = async () => {
  const response = await api.get('/models');
  return response.data.models;
};

export const getLanguages = async () => {
  const response = await api.get('/languages');
  return response.data.languages;
};

export const getLengths = async () => {
  const response = await api.get('/lengths');
  return response.data.lengths;
};

export const generatePost = async (request) => {
  const response = await api.post('/generate-post', request);
  return response.data;
};

export const getSimilarPosts = async (request) => {
  const response = await api.post('/similar-posts', request);
  return response.data.similar_posts;
};