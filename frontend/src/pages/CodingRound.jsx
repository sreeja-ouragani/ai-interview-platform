import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import { getCodingProblem, runCode, submitCode } from '../services/api';
import { motion } from 'framer-motion';
import { Play, Send, Code, Terminal, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

export default function CodingRound() {
    const navigate = useNavigate();
    const username = localStorage.getItem('username');
    const [problem, setProblem] = useState(null);
    const [code, setCode] = useState('');
    const [output, setOutput] = useState('');
    const [running, setRunning] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [results, setResults] = useState(null);

    useEffect(() => {
        const fetchProblem = async () => {
            try {
                const res = await getCodingProblem();
                // The endpoint returns { problems: [...], total: X }
                if (res.data.problems && res.data.problems.length > 0) {
                    const p = res.data.problems[0];
                    setProblem(p);
                    setCode(p.template || '');
                }
            } catch (err) {
                console.error("Coding Load Error:", err);
            }
        };
        fetchProblem();
    }, []);

    const handleRun = async () => {
        setRunning(true);
        try {
            const res = await runCode({ code, problem_id: problem.id });
            // res.data format: { result: { results: [...], passed: X, failed: Y, score: Z }, ... }
            const executionResult = res.data.result;
            if (executionResult.error) {
                setOutput(executionResult.error);
                setResults(null);
            } else {
                setOutput(`Execution complete: ${executionResult.passed} passed, ${executionResult.failed} failed.`);
                setResults(executionResult.results);
            }
        } catch (err) {
            setOutput('Error connecting to code executor.');
        }
        setRunning(false);
    };

    const handleSubmit = async () => {
        setSubmitting(true);
        try {
            const res = await submitCode({
                username,
                code,
                problem_id: problem.id,
                language: 'python'
            });
            // The score is inside res.data.result.score
            const score = res.data.result?.score || 0;
            localStorage.setItem('coding_score', score);
            navigate('/voice');
        } catch (err) {
            console.error("Submission Error:", err);
            alert('Submission failed. Check console for details.');
        }
        setSubmitting(false);
    };

    if (!problem) return (
        <div className="h-screen flex items-center justify-center bg-slate-950">
            <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
        </div>
    );

    return (
        <div className="h-screen flex flex-col bg-slate-950 text-slate-100 overflow-hidden">
            {/* Navbar */}
            <div className="h-16 border-b border-slate-800 flex items-center justify-between px-6 bg-slate-900/30 backdrop-blur-md shrink-0">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-indigo-500/10 rounded-lg flex items-center justify-center text-indigo-400">
                        <Code className="w-5 h-5" />
                    </div>
                    <span className="font-semibold text-lg">Coding Assessment</span>
                </div>
                <div className="flex items-center gap-3">
                    <button
                        onClick={handleRun}
                        disabled={running || submitting}
                        className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm font-medium transition-all disabled:opacity-50"
                    >
                        {running ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
                        Run Code
                    </button>
                    <button
                        onClick={handleSubmit}
                        disabled={submitting}
                        className="flex items-center gap-2 px-6 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-sm font-bold transition-all disabled:opacity-50"
                    >
                        {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                        Submit Solution
                    </button>
                </div>
            </div>

            <div className="flex flex-1 min-h-0">
                {/* Sidebar: Problem Description */}
                <div className="w-1/3 border-r border-slate-800 p-6 overflow-y-auto bg-slate-900/10">
                    <div className="space-y-6">
                        <div>
                            <span className="px-2 py-0.5 rounded-md bg-indigo-500/10 text-indigo-400 text-xs font-bold uppercase tracking-wider border border-indigo-500/20">
                                {problem.difficulty}
                            </span>
                            <h1 className="text-2xl font-bold mt-2">{problem.title}</h1>
                        </div>

                        <div className="prose prose-invert text-slate-400 max-w-none">
                            <p className="whitespace-pre-wrap">{problem.description}</p>
                        </div>

                        <div className="space-y-4">
                            <h3 className="font-semibold text-slate-200">Examples</h3>
                            {problem.examples?.map((ex, i) => (
                                <div key={i} className="bg-slate-900/50 border border-slate-800 p-4 rounded-xl space-y-2">
                                    <div className="text-xs text-slate-500 uppercase font-bold">Input</div>
                                    <code className="text-indigo-300">{ex.input}</code>
                                    <div className="text-xs text-slate-500 uppercase font-bold">Output</div>
                                    <code className="text-emerald-400">{ex.output}</code>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Main Content: Editor & Terminal */}
                <div className="flex-1 flex flex-col min-w-0 bg-[#1e1e1e]">
                    <div className="flex-1 min-h-0">
                        <Editor
                            height="100%"
                            defaultLanguage="python"
                            theme="vs-dark"
                            value={code}
                            onChange={setCode}
                            options={{
                                fontSize: 14,
                                minimap: { enabled: false },
                                scrollBeyondLastLine: false,
                                automaticLayout: true,
                                padding: { top: 20 }
                            }}
                        />
                    </div>

                    {/* Terminal / Output */}
                    <div className="h-1/3 border-t border-slate-800 flex flex-col shrink-0 bg-[#0f1117]">
                        <div className="h-10 border-b border-slate-800 flex items-center px-4 gap-2 bg-slate-900/50">
                            <Terminal className="w-4 h-4 text-slate-500" />
                            <span className="text-xs font-bold uppercase tracking-widest text-slate-400">Terminal</span>
                        </div>
                        <div className="flex-1 overflow-y-auto p-4 font-mono text-sm">
                            {results ? (
                                <div className="space-y-2">
                                    {results.map((res, i) => (
                                        <div key={i} className="flex items-center gap-3 p-2 rounded bg-slate-800/30">
                                            {res.passed ? <CheckCircle className="w-4 h-4 text-emerald-500" /> : <AlertCircle className="w-4 h-4 text-red-500" />}
                                            <span className="text-slate-300">Test Case {i + 1}:</span>
                                            <span className={res.passed ? 'text-emerald-400' : 'text-red-400'}>
                                                {res.passed ? 'PASSED' : `FAILED (Expected "${res.expected_output}", got "${res.actual_output}")`}
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <pre className="text-slate-400">{output || 'No output yet. Run your code to see results.'}</pre>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
