import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { getInterviewQuestion, submitVerbalAnswer, analyzeIntro } from '../services/api';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, MicOff, Volume2, VolumeX, User, Bot, ChevronRight, Loader2, Sparkles } from 'lucide-react';

export default function VoiceRound() {
    const navigate = useNavigate();
    const username = localStorage.getItem('username');
    const [step, setStep] = useState(0); // 0: intro, 1: project1, 2: project2, 3: behavioral1, 4: behavioral2
    const [question, setQuestion] = useState("Tell me about yourself and your experience.");
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState('');
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [silenceTimeout, setSilenceTimeout] = useState(null);
    const [verbalScores, setVerbalScores] = useState([]);

    const recognitionRef = useRef(null);

    useEffect(() => {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new window.webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';

            recognition.onresult = (event) => {
                let interim = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        setTranscript(prev => prev + event.results[i][0].transcript + ' ');
                    } else {
                        interim += event.results[i][0].transcript;
                    }
                }

                // Auto-silence detection logic in JS
                if (silenceTimeout) clearTimeout(silenceTimeout);
                const timeout = setTimeout(() => {
                    stopListening();
                }, 3000); // 3 seconds of silence
                setSilenceTimeout(timeout);
            };

            recognition.onend = () => setIsListening(false);
            recognitionRef.current = recognition;
        }

        // Initial welcome speech
        speak(question);

        return () => {
            if (recognitionRef.current) recognitionRef.current.stop();
        };
    }, []);

    const speak = (text) => {
        if (!window.speechSynthesis) return;
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.onstart = () => setIsSpeaking(true);
        utterance.onend = () => setIsSpeaking(false);
        window.speechSynthesis.speak(utterance);
    };

    const startListening = () => {
        setTranscript('');
        setIsListening(true);
        if (recognitionRef.current) recognitionRef.current.start();
    };

    const stopListening = () => {
        setIsListening(false);
        if (recognitionRef.current) recognitionRef.current.stop();
    };

    const handleNext = async () => {
        setLoading(true);
        try {
            const currentAnswer = transcript.trim();
            setHistory([...history, { question, answer: currentAnswer }]);

            let nextStep = step + 1;
            let nextQuestion = "";

            if (step === 0) {
                // Just finished intro
                const resIntro = await analyzeIntro({ username, answer: currentAnswer });
                const introScore = resIntro.data.analysis?.score || resIntro.data.analysis?.["Overall Score"] || 0;
                setVerbalScores(prev => [...prev, introScore]);

                const res = await getInterviewQuestion('project', { username, conversation_history: history, tone: 'professional' });
                nextQuestion = res.data.question;
            } else if (step < 2) {
                // Project questions
                const resAnsw = await submitVerbalAnswer({ username, question, answer: currentAnswer });
                const score = resAnsw.data.analysis?.score || resAnsw.data.analysis?.["Overall Score"] || 0;
                setVerbalScores(prev => [...prev, score]);

                const res = await getInterviewQuestion('project', { username, conversation_history: history, tone: 'professional' });
                nextQuestion = res.data.question;
            } else if (step < 4) {
                // Behavioral questions
                const resAnsw = await submitVerbalAnswer({ username, question, answer: currentAnswer });
                const score = resAnsw.data.analysis?.score || resAnsw.data.analysis?.["Overall Score"] || 0;
                setVerbalScores(prev => [...prev, score]);

                const res = await getInterviewQuestion('hr', { username, conversation_history: history, tone: 'friendly' });
                nextQuestion = res.data.question;
            } else {
                // Final answer of last round
                const resAnsw = await submitVerbalAnswer({ username, question, answer: currentAnswer });
                const score = resAnsw.data.analysis?.score || resAnsw.data.analysis?.["Overall Score"] || 0;
                const finalScores = [...verbalScores, score];
                const avg = finalScores.reduce((a, b) => a + b, 0) / finalScores.length;
                localStorage.setItem('verbal_score', Math.round(avg));

                // Complete
                navigate('/results');
                return;
            }

            setStep(nextStep);
            setQuestion(nextQuestion);
            setTranscript('');
            speak(nextQuestion);
        } catch (err) {
            console.error(err);
            alert('Error advancing round');
        }
        setLoading(false);
    };

    return (
        <div className="h-screen bg-slate-950 flex flex-col items-center justify-center p-6 relative overflow-hidden">
            {/* Background Glow */}
            <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full blur-[120px] transition-all duration-1000 ${isListening ? 'bg-indigo-500/10' : 'bg-transparent'}`} />

            <div className="z-10 w-full max-w-2xl space-y-12">
                {/* Step Indicator */}
                <div className="flex justify-center gap-2">
                    {[0, 1, 2, 3, 4].map((i) => (
                        <div key={i} className={`h-1.5 rounded-full transition-all duration-500 ${step === i ? 'w-8 bg-indigo-500' : 'w-2 bg-slate-800'}`} />
                    ))}
                </div>

                {/* AI Interaction Zone */}
                <div className="space-y-8 text-center">
                    <motion.div
                        animate={{
                            scale: isSpeaking ? [1, 1.05, 1] : 1,
                        }}
                        transition={{ repeat: Infinity, duration: 2 }}
                        className={`w-32 h-32 rounded-full mx-auto flex items-center justify-center border-2 transition-all duration-500 ${isSpeaking ? 'bg-indigo-500/20 border-indigo-400' : 'bg-slate-900 border-slate-800'}`}
                    >
                        {isSpeaking ? (
                            <Volume2 className="w-12 h-12 text-indigo-400" />
                        ) : (
                            <Bot className="w-12 h-12 text-slate-500" />
                        )}
                    </motion.div>

                    <AnimatePresence mode="wait">
                        <motion.h2
                            key={question}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="text-2xl md:text-3xl font-medium leading-relaxed max-w-xl mx-auto"
                        >
                            {question}
                        </motion.h2>
                    </AnimatePresence>
                </div>

                {/* User Interaction Zone */}
                <div className="space-y-6">
                    <div className={`min-h-[100px] p-6 rounded-2xl bg-slate-900/50 border transition-all ${isListening ? 'border-indigo-500/50 shadow-[0_0_30px_-10px_rgba(99,102,241,0.2)]' : 'border-slate-800'}`}>
                        {transcript ? (
                            <p className="text-lg text-slate-200">{transcript}</p>
                        ) : (
                            <p className="text-slate-500 italic text-center">
                                {isListening ? "Listening... continue speaking." : "Ready to speak? Click the mic below."}
                            </p>
                        )}
                    </div>

                    <div className="flex justify-center items-center gap-6">
                        <button
                            onClick={isListening ? stopListening : startListening}
                            className={`w-20 h-20 rounded-full flex items-center justify-center transition-all ${isListening ? 'bg-red-500/20 border-2 border-red-500 text-red-500' : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-500/20'}`}
                        >
                            {isListening ? <MicOff className="w-8 h-8" /> : <Mic className="w-8 h-8" />}
                        </button>

                        {(transcript || step >= 0) && (
                            <button
                                disabled={loading || isListening}
                                onClick={handleNext}
                                className="px-8 py-3 bg-white text-slate-950 font-bold rounded-xl flex items-center gap-2 hover:bg-slate-100 transition-all disabled:opacity-50"
                            >
                                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : step === 4 ? "Finish Interview" : "Next Question"}
                                <ChevronRight className="w-5 h-5" />
                            </button>
                        )}
                    </div>
                </div>
            </div>

            {/* Visualizer Lines (Simulated) */}
            <div className="absolute bottom-10 left-0 right-0 h-20 flex items-end justify-center gap-1 opacity-20 pointer-events-none">
                {Array.from({ length: 40 }).map((_, i) => (
                    <motion.div
                        key={i}
                        animate={{ height: isListening ? Math.random() * 80 + 20 : 5 }}
                        transition={{ repeat: Infinity, duration: 0.1 }}
                        className="w-1 bg-indigo-500 rounded-full"
                    />
                ))}
            </div>
        </div>
    );
}
