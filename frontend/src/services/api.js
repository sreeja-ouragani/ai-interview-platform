import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:5000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const startInterview = (username, data) => api.post(`/interview/start/${username}`, data);
export const registerUser = (data) => api.post('/user/register', data);
export const uploadResume = (username, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/resume/upload/${username}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    });
};
export const getMCQQuestions = () => api.get('/mcq/questions?difficulty=all&count=10');
export const submitMCQ = (data) => api.post('/mcq/evaluate', data);
export const getCodingProblem = () => api.get('/coding/problems?difficulty=Easy');
export const runCode = (data) => api.post('/coding/execute', data);
export const submitCode = (data) => api.post('/coding/submit', data);
export const analyzeIntro = (data) => api.post('/interview/intro', data);
export const getInterviewQuestion = (type, data) => api.post(`/interview/${type}/question`, data);
export const submitVerbalAnswer = (data) => api.post('/interview/hr/answer', data); // Generic analysis
export const matchJob = (username, data) => api.post(`/resume/match/${username}`, data);
export const completeInterview = (username, data) => api.post(`/interview/complete/${username}`, data);

export default api;
