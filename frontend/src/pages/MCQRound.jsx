import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMCQQuestions, submitMCQ } from '../services/api';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronRight, Timer, HelpCircle, CheckCircle2 } from 'lucide-react';

export default function MCQRound() {
    const navigate = useNavigate();
    const username = localStorage.getItem('username');
    const [questions, setQuestions] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [selectedAnswers, setSelectedAnswers] = useState({});
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [timeLeft, setTimeLeft] = useState(600); // 10 minutes

    useEffect(() => {
        const fetchQuestions = async () => {
            try {
                const res = await getMCQQuestions();
                // The endpoint returns { questions: [...] }
                setQuestions(res.data.questions || []);
            } catch (err) {
                console.error("MCQ Load Error:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchQuestions();
    }, []);

    useEffect(() => {
        if (timeLeft <= 0) handleSubmit();
        const timer = setInterval(() => setTimeLeft(t => t - 1), 1000);
        return () => clearInterval(timer);
    }, [timeLeft]);

    const handleSubmit = async () => {
        setSubmitting(true);
        try {
            const answersObj = {};
            questions.forEach((q, idx) => {
                answersObj[q.id] = selectedAnswers[idx] || "";
            });
            const res = await submitMCQ({ username, answers: answersObj });
            // The backend returns { evaluation: { score_percentage: X }, ... }
            const score = res.data.evaluation?.score_percentage || 0;
            localStorage.setItem('mcq_score', score);
            navigate('/coding');
        } catch (err) {
            console.error(err);
            alert('Failed to submit MCQ');
        }
        setSubmitting(false);
    };

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    if (loading) return (
        <div className="h-screen flex items-center justify-center bg-slate-950">
            <div className="flex flex-col items-center gap-4">
                <div className="w-12 h-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin"></div>
                <p className="text-slate-400 animate-pulse">Prepping your technical assessment...</p>
            </div>
        </div>
    );

    const currentQ = questions[currentIndex];

    return (
        <div className="min-h-screen bg-slate-950 text-white p-4 md:p-8 flex flex-col items-center">
            <div className="w-full max-w-4xl space-y-8">
                {/* Header */}
                <div className="flex justify-between items-center bg-slate-900/50 border border-slate-800 p-4 rounded-xl backdrop-blur-sm">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-indigo-500/10 rounded-lg flex items-center justify-center text-indigo-400">
                            <HelpCircle className="w-6 h-6" />
                        </div>
                        <div>
                            <h3 className="font-semibold">Technical Round</h3>
                            <p className="text-xs text-slate-500">Question {currentIndex + 1} of {questions.length}</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border ${timeLeft < 60 ? 'bg-red-500/10 border-red-500/20 text-red-400' : 'bg-slate-800 border-slate-700 text-slate-300'}`}>
                            <Timer className="w-4 h-4" />
                            <span className="font-mono font-medium">{formatTime(timeLeft)}</span>
                        </div>
                    </div>
                </div>

                {/* Progress Bar */}
                <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
                    <motion.div
                        className="h-full bg-indigo-500"
                        initial={{ width: 0 }}
                        animate={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
                    />
                </div>

                {/* Question Area */}
                <AnimatePresence mode="wait">
                    <motion.div
                        key={currentIndex}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        className="bg-slate-900/40 border border-slate-800 p-8 rounded-2xl space-y-8"
                    >
                        <h2 className="text-2xl font-medium leading-relaxed">
                            {currentQ.question}
                        </h2>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {currentQ.options.map((option, idx) => {
                                const label = String.fromCharCode(65 + idx);
                                const isSelected = selectedAnswers[currentIndex] === label;
                                return (
                                    <button
                                        key={idx}
                                        onClick={() => setSelectedAnswers({ ...selectedAnswers, [currentIndex]: label })}
                                        className={`group relative p-6 rounded-xl border text-left transition-all ${isSelected
                                            ? 'bg-indigo-500/10 border-indigo-500 shadow-[0_0_20px_-5px_rgba(99,102,241,0.2)]'
                                            : 'bg-slate-900 border-slate-800 hover:border-slate-700'
                                            }`}
                                    >
                                        <div className="flex items-start gap-4">
                                            <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold transition-all ${isSelected ? 'bg-indigo-500 text-white' : 'bg-slate-800 text-slate-400 group-hover:bg-slate-700'
                                                }`}>
                                                {label}
                                            </div>
                                            <span className={`text-lg pt-0.5 ${isSelected ? 'text-white' : 'text-slate-300'}`}>
                                                {option}
                                            </span>
                                        </div>
                                    </button>
                                );
                            })}
                        </div>
                    </motion.div>
                </AnimatePresence>

                {/* Navigation */}
                <div className="flex justify-between items-center pt-4">
                    <button
                        disabled={currentIndex === 0}
                        onClick={() => setCurrentIndex(currentIndex - 1)}
                        className="px-6 py-2.5 rounded-lg border border-slate-800 text-slate-400 hover:bg-slate-900 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                    >
                        Previous
                    </button>

                    <div className="flex gap-4">
                        {currentIndex === questions.length - 1 ? (
                            <button
                                onClick={handleSubmit}
                                disabled={submitting}
                                className="group px-8 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-semibold flex items-center gap-2 transition-all shadow-lg shadow-indigo-500/20"
                            >
                                {submitting ? 'Submitting...' : 'Complete Round'}
                                <CheckCircle2 className="w-5 h-5" />
                            </button>
                        ) : (
                            <button
                                onClick={() => setCurrentIndex(currentIndex + 1)}
                                className="group px-8 py-2.5 bg-white text-slate-950 hover:bg-slate-100 rounded-lg font-semibold flex items-center gap-2 transition-all"
                            >
                                Next Question
                                <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
