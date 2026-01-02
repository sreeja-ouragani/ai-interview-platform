import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser, uploadResume, matchJob } from '../services/api';
import { Upload, ChevronRight, CheckCircle2, AlertCircle, Sparkles, Brain, Code, Target } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function Registration() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({ name: '', experience: 'Junior', role: 'Full Stack Developer', jd: '' });
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [analysis, setAnalysis] = useState(null); // { skills: {}, match: {} }
    const [showAnalysis, setShowAnalysis] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await registerUser({
                username: formData.name,
                experience_level: formData.experience,
                target_role: formData.role,
                job_description: formData.jd
            });

            let skills = null;
            let match = null;

            if (file) {
                const resUpload = await uploadResume(formData.name, file);
                skills = resUpload.data.skills;

                if (formData.jd) {
                    const resMatch = await matchJob(formData.name, { job_description: formData.jd });
                    match = resMatch.data.match_result;
                }
            }

            localStorage.setItem('username', formData.name);

            if (skills || match) {
                setAnalysis({ skills, match });
                setShowAnalysis(true);
            } else {
                navigate('/mcq');
            }
        } catch (error) {
            console.error(error);
            alert('Registration failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    if (showAnalysis) {
        return (
            <div className="min-h-screen bg-slate-950 text-white p-6 flex flex-col items-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="w-full max-w-4xl space-y-8 mt-10"
                >
                    <div className="text-center space-y-4">
                        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-sm font-bold">
                            <Brain className="w-4 h-4" />
                            AI Resume Analysis Complete
                        </div>
                        <h1 className="text-4xl font-extrabold tracking-tight">Your Talent Profile</h1>
                        <p className="text-slate-400">Here's what our AI extracted from your resume and how you match the role.</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {/* Extracted Skills */}
                        {analysis.skills && (
                            <div className="bg-slate-900/50 border border-slate-800 p-8 rounded-3xl space-y-6">
                                <h3 className="text-xl font-bold flex items-center gap-2">
                                    <Code className="w-6 h-6 text-indigo-400" />
                                    Extracted Skills
                                </h3>

                                <div className="space-y-4">
                                    <div>
                                        <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Technical</span>
                                        <div className="flex flex-wrap gap-2 mt-2">
                                            {analysis.skills.technical_skills?.map((s, i) => (
                                                <span key={i} className="px-3 py-1 bg-slate-800 rounded-lg text-sm text-slate-300 border border-slate-700">{s}</span>
                                            ))}
                                        </div>
                                    </div>
                                    <div>
                                        <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Soft Skills</span>
                                        <div className="flex flex-wrap gap-2 mt-2">
                                            {analysis.skills.soft_skills?.map((s, i) => (
                                                <span key={i} className="px-3 py-1 bg-slate-800 rounded-lg text-sm text-slate-300">{s}</span>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Skill Gap Analysis */}
                        {analysis.match && (
                            <div className="bg-slate-900/50 border border-slate-800 p-8 rounded-3xl space-y-6">
                                <div className="flex justify-between items-center">
                                    <h3 className="text-xl font-bold flex items-center gap-2">
                                        <Target className="w-6 h-6 text-emerald-400" />
                                        Role Match
                                    </h3>
                                    <span className="text-2xl font-black text-emerald-400">{analysis.match.match_score}%</span>
                                </div>

                                <div className="space-y-4">
                                    <div>
                                        <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Matching Proficiencies</span>
                                        <div className="flex flex-wrap gap-2 mt-2">
                                            {analysis.match.matching_skills?.map((s, i) => (
                                                <span key={i} className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-lg text-sm">{s}</span>
                                            ))}
                                        </div>
                                    </div>
                                    {analysis.match.missing_skills?.length > 0 && (
                                        <div>
                                            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest text-amber-500/70">Potential Skill Gaps</span>
                                            <div className="flex flex-wrap gap-2 mt-2">
                                                {analysis.match.missing_skills?.map((s, i) => (
                                                    <span key={i} className="px-3 py-1 bg-amber-500/10 text-amber-500 border border-amber-500/20 rounded-lg text-sm">{s}</span>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="flex justify-center pt-8">
                        <button
                            onClick={() => navigate('/mcq')}
                            className="group relative px-12 py-4 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-2xl transition-all shadow-[0_0_40px_-10px_rgba(99,102,241,0.5)] overflow-hidden"
                        >
                            <div className="relative z-10 flex items-center gap-3">
                                Start Technical Assessment
                                <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                            </div>
                            <motion.div
                                className="absolute inset-0 bg-gradient-to-r from-white/10 to-transparent"
                                animate={{ x: ['-100%', '200%'] }}
                                transition={{ repeat: Infinity, duration: 1.5, ease: 'linear' }}
                            />
                        </button>
                    </div>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-950 p-4">
            <div className="w-full max-w-md space-y-8">
                <div className="text-center">
                    <h2 className="text-3xl font-bold tracking-tight">Create Profile</h2>
                    <p className="text-slate-400 mt-2">Let's personalize your interview experience</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6 mt-8">
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-1">Full Name</label>
                            <input
                                required
                                type="text"
                                className="w-full bg-slate-900 border border-slate-800 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all placeholder:text-slate-600"
                                placeholder="e.g. Alex Johnson"
                                value={formData.name}
                                onChange={e => setFormData({ ...formData, name: e.target.value })}
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-1">Experience</label>
                                <select
                                    className="w-full bg-slate-900 border border-slate-800 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                                    value={formData.experience}
                                    onChange={e => setFormData({ ...formData, experience: e.target.value })}
                                >
                                    <option>Fresher</option>
                                    <option>Junior</option>
                                    <option>Mid</option>
                                    <option>Senior</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-1">Role</label>
                                <input
                                    type="text"
                                    className="w-full bg-slate-900 border border-slate-800 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                                    value={formData.role}
                                    onChange={e => setFormData({ ...formData, role: e.target.value })}
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-1">Resume (Required for Analysis)</label>
                            <div className={`border-2 border-dashed rounded-lg p-6 hover:border-indigo-500/50 transition-colors cursor-pointer text-center ${file ? 'border-indigo-500/50 bg-indigo-500/5' : 'border-slate-800'}`}
                                onClick={() => document.getElementById('file-upload').click()}>
                                <input id="file-upload" type="file" className="hidden" onChange={e => setFile(e.target.files[0])} />
                                <Upload className={`mx-auto h-8 w-8 mb-2 ${file ? 'text-indigo-400' : 'text-slate-500'}`} />
                                <p className={`text-sm ${file ? 'text-slate-200 font-medium' : 'text-slate-400'}`}>
                                    {file ? file.name : "Click to upload PDF"}
                                </p>
                                {file && <span className="text-[10px] text-indigo-400 uppercase font-bold mt-1 block">Ready to analyze</span>}
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-1">Job Description (Required for Match)</label>
                            <textarea
                                className="w-full bg-slate-900 border border-slate-800 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 h-24 resize-none placeholder:text-slate-600"
                                placeholder="Paste JD here for better context..."
                                value={formData.jd}
                                onChange={e => setFormData({ ...formData, jd: e.target.value })}
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3.5 rounded-lg transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? (
                            <>
                                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                Analyzing Profile...
                            </>
                        ) : (
                            <>
                                Continue to Analysis
                                <ChevronRight className="w-4 h-4" />
                            </>
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
}
