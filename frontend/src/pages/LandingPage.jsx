import { ArrowRight, Sparkles } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

export default function LandingPage() {
    const navigate = useNavigate();

    return (
        <div className="h-screen flex flex-col items-center justify-center bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/50 via-slate-950 to-slate-950 relative overflow-hidden">
            <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 brightness-100 contrast-150 mix-blend-overlay"></div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="z-10 text-center space-y-8 max-w-4xl px-4"
            >
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-sm font-medium">
                    <Sparkles className="w-4 h-4" />
                    <span>AI-Powered Interview Intelligence</span>
                </div>

                <h1 className="text-6xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-b from-white to-white/60 tracking-tight">
                    Master Your Next <br />
                    <span className="text-indigo-500">Technical Interview</span>
                </h1>

                <p className="text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
                    Experience a real-time simulation with AI that adapts to your skills.
                    From coding challenges to behavioral questions, get instant feedback and level up.
                </p>

                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => navigate('/register')}
                    className="group relative inline-flex items-center gap-3 px-8 py-4 bg-white text-slate-950 rounded-full font-semibold text-lg hover:bg-indigo-50 transition-colors shadow-[0_0_40px_-10px_rgba(255,255,255,0.3)]"
                >
                    Start Interview
                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </motion.button>
            </motion.div>
        </div>
    );
}
