import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import Registration from './pages/Registration';
import MCQRound from './pages/MCQRound';
import CodingRound from './pages/CodingRound';
import VoiceRound from './pages/VoiceRound';
import Results from './pages/Results';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-950 text-white font-sans selection:bg-purple-500/30">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/register" element={<Registration />} />
          <Route path="/mcq" element={<MCQRound />} />
          <Route path="/coding" element={<CodingRound />} />
          <Route path="/voice" element={<VoiceRound />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
