/*import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// Get recommendations for a student
export const getRecommendations = async (studentId, topK = 6) => {
  const res = await API.post(`/recommendations?student_id=${studentId}&top_k=${topK}`);
  return res.data;
};*/

import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// Get recommendations for a student
export const getRecommendations = async (studentId, topK = 6) => {
  const res = await API.post("/recommendations", {
    student_id: studentId,
    top_k: topK,
  });
  return res.data;
};