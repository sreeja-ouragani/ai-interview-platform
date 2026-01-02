import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { motion } from 'framer-motion';
import { Award, TrendingUp, BookOpen, AlertCircle, Share2, CheckCircle2, Mic, Sparkles } from 'lucide-react';

export default function Results() {
    const navigate = useNavigate();
    const username = localStorage.getItem('username');
    const [feedback, setFeedback] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchResults = async () => {
            try {
                const mcq = parseFloat(localStorage.getItem('mcq_score')) || 0;
                const coding = parseFloat(localStorage.getItem('coding_score')) || 0;
                const verbal = parseFloat(localStorage.getItem('verbal_score')) || 0;

                const overall = Math.round((mcq + coding + verbal) / 3);

                const res = await api.post(`/interview/complete/${username}`, {
                    interview_data: {
                        mcq_score: mcq,
                        coding_score: coding,
                        verbal_score: verbal,
                        overall_score: overall,
                        rounds_completed: ["Technical", "Coding", "Verbal"]
                    }
                });
                setFeedback(res.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchResults();
    }, []);

    if (loading) return (
        <div className="h-screen flex flex-col items-center justify-center bg-slate-950 gap-6">
            <motion.div
                animate={{ rotate: 360 }}
                transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                className="w-16 h-16 border-t-4 border-indigo-500 rounded-full"
            />
            <div className="text-center space-y-2">
                <h2 className="text-xl font-bold">Generating Final Assessment</h2>
                <p className="text-slate-400">Aggregating scores and analyzing performance...</p>
            </div>
        </div>
    );

    const score = Math.round(feedback?.overall_score || 0);

    return (
        <div className="min-h-screen bg-slate-950 text-white p-6 md:p-12">
            <div className="max-w-5xl mx-auto space-y-10">
                {/* Hero Score Section */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="lg:col-span-1 bg-gradient-to-br from-indigo-600 to-purple-700 p-1 rounded-3xl"
                    >
                        <div className="bg-slate-950 h-full w-full rounded-[20px] flex flex-col items-center justify-center p-8 text-center space-y-4">
                            <Award className="w-12 h-12 text-indigo-400" />
                            <h1 className="text-5xl font-extrabold">{score}%</h1>
                            <p className="text-slate-400 uppercase tracking-widest text-sm font-bold">Overall Rating</p>
                            <div className={`mt-4 px-4 py-1.5 rounded-full text-sm font-bold ${score >= 70 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>
                                {score >= 70 ? 'Shortlisted' : 'Need Improvement'}
                            </div>
                        </div>
                    </motion.div>

                    <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl flex flex-col justify-between">
                            <TrendingUp className="w-6 h-6 text-indigo-400" />
                            <div>
                                <div className="text-3xl font-bold">{Math.round(parseFloat(localStorage.getItem('mcq_score') || 0))}%</div>
                                <div className="text-slate-500 text-sm">MCQ Performance</div>
                            </div>
                        </div>
                        <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl flex flex-col justify-between">
                            <TrendingUp className="w-6 h-6 text-purple-400" />
                            <div>
                                <div className="text-3xl font-bold">{Math.round(parseFloat(localStorage.getItem('coding_score') || 0))}%</div>
                                <div className="text-slate-500 text-sm">Coding Proficiency</div>
                            </div>
                        </div>
                        <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl flex flex-col justify-between">
                            <Mic className="w-6 h-6 text-emerald-400" />
                            <div>
                                <div className="text-3xl font-bold">{Math.round(parseFloat(localStorage.getItem('verbal_score') || 0))}%</div>
                                <div className="text-slate-500 text-sm">Verbal Communication</div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Overall Summary */}
                {feedback?.feedback?.summary && (
                    <div className="bg-slate-900/30 border border-slate-800 p-8 rounded-3xl">
                        <h3 className="text-xl font-bold mb-4">Executive Summary</h3>
                        <p className="text-slate-400 leading-relaxed">{feedback.feedback.summary}</p>
                    </div>
                )}

                {/* Detailed Feedback */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Strengths */}
                    <section className="space-y-4">
                        <h3 className="text-xl font-bold flex items-center gap-2">
                            <CheckCircle2 className="w-6 h-6 text-emerald-500" />
                            Key Strengths
                        </h3>
                        <div className="space-y-3">
                            {(feedback?.feedback?.strengths || []).map((s, i) => (
                                <div key={i} className="bg-slate-900/40 border border-slate-800/50 p-4 rounded-xl text-slate-300">
                                    {s}
                                </div>
                            ))}
                        </div>
                    </section>

                    {/* Weaknesses */}
                    <section className="space-y-4">
                        <h3 className="text-xl font-bold flex items-center gap-2">
                            <AlertCircle className="w-6 h-6 text-amber-500" />
                            Focus Areas
                        </h3>
                        <div className="space-y-3">
                            {(feedback?.feedback?.weaknesses || []).map((w, i) => (
                                <div key={i} className="bg-slate-900/40 border border-slate-800/50 p-4 rounded-xl text-slate-300">
                                    {w}
                                </div>
                            ))}
                        </div>
                    </section>
                </div>

                {/* Learning Resources */}
                {feedback?.feedback?.recommendations && (
                    <section className="bg-slate-900/30 border border-slate-800 p-8 rounded-3xl space-y-6">
                        <h3 className="text-2xl font-bold flex items-center gap-3">
                            <BookOpen className="w-7 h-7 text-indigo-400" />
                            Personalized Learning Path
                        </h3>
                        <div className="prose prose-invert max-w-none text-slate-400 leading-relaxed">
                            {feedback.feedback.recommendations}
                        </div>

                        {feedback?.feedback?.action_plan && (
                            <div className="mt-8 p-6 bg-indigo-500/5 rounded-2xl border border-indigo-500/10">
                                <h4 className="text-indigo-400 font-bold mb-2 flex items-center gap-2">
                                    <Sparkles className="w-4 h-4" />
                                    Step-by-Step Action Plan
                                </h4>
                                <div className="text-slate-400 whitespace-pre-wrap">{feedback.feedback.action_plan}</div>
                            </div>
                        )}

                        <div className="pt-4 flex flex-wrap gap-4">
                            <button className="flex items-center gap-2 bg-indigo-600 px-6 py-2.5 rounded-full font-bold hover:bg-indigo-500 transition-all">
                                <Sparkles className="w-4 h-4" />
                                Explore Tutorials
                            </button>
                            <button className="flex items-center gap-2 border border-slate-700 px-6 py-2.5 rounded-full font-bold hover:bg-slate-800 transition-all">
                                <Share2 className="w-4 h-4" />
                                Share Results
                            </button>
                        </div>
                    </section>
                )}

                <div className="pt-10 border-t border-slate-900 text-center">
                    <button
                        onClick={() => navigate('/')}
                        className="text-indigo-400 font-bold hover:text-indigo-300 transition-all"
                    >
                        Start New Session
                    </button>
                </div>
            </div>
        </div>
    );
}
