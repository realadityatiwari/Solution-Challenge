'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldAlert, Video, Activity, Gavel, CheckCircle2, AlertTriangle, Eye, Shield, Link2, Clock, X, Terminal, FileText, Image as ImageIcon, UploadCloud, FileVideo, Send, Check } from 'lucide-react';
import { generateTakedown, analyzeNewsAction, uploadFingerprintAction } from './actions';

export default function SOCDashboard() {
  const [selectedViolation, setSelectedViolation] = useState<any | null>(null);
  const [takedownDraft, setTakedownDraft] = useState<string | null>(null);
  const [isDrafting, setIsDrafting] = useState(false);
  const [timeStr, setTimeStr] = useState('');

  useEffect(() => {
    setTimeStr(new Date().toLocaleTimeString());
    const t = setInterval(() => setTimeStr(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(t);
  }, []);

  // Asset Fingerprints State
  const [fingerprintFile, setFingerprintFile] = useState<File | null>(null);
  const [fingerprintVideoId, setFingerprintVideoId] = useState("");
  const [isUploadingAsset, setIsUploadingAsset] = useState(false);
  const [indexedAssets, setIndexedAssets] = useState<{id: string, name: string}[]>([
    { id: "LAL_MIA_03192026_CAM1", name: "Lakers vs Heat Q1 Broadcast" },
    { id: "PHX_SAS_03192026_FEED", name: "Suns vs Spurs 4th Quarter Run" }
  ]);

  const handleFingerprintFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFingerprintFile(e.target.files[0]);
    }
  };

  const handleUploadAsset = async () => {
    if (!fingerprintFile || !fingerprintVideoId.trim()) return;
    setIsUploadingAsset(true);
    const formData = new FormData();
    formData.append('video_id', fingerprintVideoId);
    formData.append('file', fingerprintFile);
    
    const result = await uploadFingerprintAction(formData);
    if (result && result.status === 'success') {
       setIndexedAssets(prev => [{ id: result.video_id, name: fingerprintFile.name }, ...prev]);
       setFingerprintFile(null);
       setFingerprintVideoId("");
    }
    setIsUploadingAsset(false);
  };

  // Takedown Queue State
  const [takedownQueue, setTakedownQueue] = useState<{id: string, notice: string, violation: any}[]>([]);

  const handleTransmitToISP = (id: string) => {
    setTakedownQueue(prev => prev.filter(item => item.id !== id));
  };

  const [activeTab, setActiveTab] = useState('feed');
  const [newsText, setNewsText] = useState("");
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isScanningNews, setIsScanningNews] = useState(false);
  const [newsReport, setNewsReport] = useState<any | null>(null);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const removeImage = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
  };

  const handleScanNews = async () => {
    if (!newsText.trim() && !selectedImage) return;
    setIsScanningNews(true);
    setNewsReport(null);
    
    const formData = new FormData();
    if (newsText.trim()) formData.append('news_text', newsText);
    if (selectedImage) formData.append('file', selectedImage);
    
    const result = await analyzeNewsAction(formData);
    if (result && result.report) {
       setNewsReport(result.report);
    }
    setIsScanningNews(false);
  };

  // Mocked Data representing what was caught by the Sentry + Validator pipeline
  const [violations, setViolations] = useState([
    {
      id: "V-9921A",
      title: "LAKERS at HEAT | FULL GAME HIGHLIGHTS | March 19, 2026",
      channel: "NBA", // Should be flagged as protected channel
      url: "https://www.youtube.com/watch?v=SyXKBWaUV60",
      match_score: 99.1,
      timestamp: "Just now",
      official_asset: "LAL_MIA_03192026_CAM1",
      official_thumb: "https://images.unsplash.com/photo-1542652694-40abf526446e?auto=format&fit=crop&q=80&w=200",
      pirated_thumb: "https://images.unsplash.com/photo-1504450758481-7338eba7524a?auto=format&fit=crop&q=80&w=200"
    },
    {
      id: "V-9921B",
      title: "SUNS at SPURS | 4TH QUARTER RUN",
      channel: "HoopsFan99", 
      url: "https://www.youtube.com/watch?v=xqV3-vk-Bzo",
      match_score: 94.3,
      timestamp: "2 mins ago",
      official_asset: "PHX_SAS_03192026_FEED",
      official_thumb: "https://images.unsplash.com/photo-1519861531473-9200262188bf?auto=format&fit=crop&q=80&w=200",
      pirated_thumb: "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&q=80&w=200"
    }
  ]);

  const handleDismiss = (id: string) => {
    setViolations(prev => prev.filter(v => v.id !== id));
  };

  const handleSendNotice = () => {
    if (selectedViolation && takedownDraft) {
      setTakedownQueue(prev => [{
         id: selectedViolation.id,
         notice: takedownDraft,
         violation: selectedViolation
      }, ...prev]);
      handleDismiss(selectedViolation.id);
    }
    closeTakedownDraft();
  };

  const handleGenerateTakedown = async (violation: any) => {
    setIsDrafting(true);
    const res = await generateTakedown(violation);
    setTakedownDraft(res.text ?? null);
    setIsDrafting(false);
  };

  const closeTakedownDraft = () => {
    setTakedownDraft(null);
    setSelectedViolation(null);
  };

  return (
    <div className="flex h-screen bg-[#050505] text-slate-300 font-sans selection:bg-blue-500/30 overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800/60 bg-[#0a0a0a] flex flex-col relative z-20 shadow-2xl">
        <div className="p-6 border-b border-slate-800/60">
          <div className="flex items-center gap-2 mb-1">
            <Shield className="w-6 h-6 text-blue-500" />
            <h1 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300 tracking-tight">
              SOC Nexus
            </h1>
          </div>
          <p className="text-[10px] text-slate-500 font-mono tracking-widest uppercase ml-8">Antigravity Shield</p>
        </div>
        
        <nav className="flex-1 px-3 py-6 space-y-1">
          <SidebarItem active={activeTab === 'feed'} onClick={() => setActiveTab('feed')} icon={<Activity className="w-4 h-4" />}>Live Feed</SidebarItem>
          <SidebarItem active={activeTab === 'news'} onClick={() => setActiveTab('news')} icon={<FileText className="w-4 h-4" />}>News Scanner</SidebarItem>
          <SidebarItem active={activeTab === 'fingerprints'} onClick={() => setActiveTab('fingerprints')} icon={<Video className="w-4 h-4" />}>Asset Fingerprints</SidebarItem>
          <SidebarItem active={activeTab === 'queue'} onClick={() => setActiveTab('queue')} icon={<ShieldAlert className="w-4 h-4" />}>Takedown Queue</SidebarItem>
          <SidebarItem active={activeTab === 'logs'} onClick={() => setActiveTab('logs')} icon={<Terminal className="w-4 h-4" />}>Agent Logs</SidebarItem>
        </nav>
        
        <div className="p-4 m-4 rounded-xl bg-gradient-to-br from-blue-900/20 to-slate-900 border border-blue-500/20">
          <div className="text-xs text-blue-400 mb-2 flex items-center gap-1.5 font-medium"><div className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse" /> Sentry Active</div>
          <p className="text-xs text-slate-400">Scanning YouTube endpoints for protected assets in real-time.</p>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative z-10">
        {/* Background Mesh */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(37,99,235,0.05),transparent_50%)] pointer-events-none" />

        {/* Top Header */}
        <header className="h-16 border-b border-slate-800/60 bg-[#0a0a0a]/80 backdrop-blur-md flex items-center justify-between px-8 sticky top-0 z-10">
          <div className="flex items-center gap-4">
            <h2 className="text-sm font-semibold tracking-wide text-slate-100 uppercase">
              {activeTab === 'feed' && 'Live Violation Feed'}
              {activeTab === 'news' && 'News Source Scanner'}
              {activeTab === 'fingerprints' && 'Asset Fingerprints'}
              {activeTab === 'queue' && 'Takedown Queue'}
              {activeTab === 'logs' && 'Agent Logs'}
            </h2>
            {activeTab === 'feed' && (
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-red-500/10 text-red-400 border border-red-500/20">
                {violations.length} ALERTS
              </span>
            )}
          </div>
          <div className="flex items-center gap-4 opacity-80 text-sm">
            <span className="flex items-center gap-2"><Clock className="w-4 h-4" /> {timeStr}</span>
          </div>
        </header>

        {/* Feed Content */}
        <div className="flex-1 overflow-auto p-8 relative">
          
          <div className="max-w-5xl mx-auto space-y-6">
            {activeTab === 'feed' ? (
              <AnimatePresence>
              {violations.map((v, idx) => (
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  key={v.id} 
                  className="bg-[#0a0a0a] border border-slate-800/60 hover:border-slate-700 rounded-xl overflow-hidden transition-colors shadow-none hover:shadow-[0_0_30px_rgba(0,0,0,0.5)]"
                >
                  {/* Header */}
                  <div className="px-6 py-4 border-b border-slate-800/60 flex justify-between items-start bg-slate-900/20">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <AlertTriangle className="w-4 h-4 text-red-400" />
                        <h3 className="text-sm font-bold text-slate-200">Match Detected: {v.id}</h3>
                      </div>
                      <p className="text-xs text-slate-500 font-mono">{v.url}</p>
                    </div>
                    
                    <div className="flex flex-col items-end">
                      <span className="text-xs text-slate-400 mb-1">{v.timestamp}</span>
                      <span className="px-2 py-1 rounded text-xs font-bold bg-amber-500/10 text-amber-500 border border-amber-500/20 shadow-[0_0_10px_rgba(245,158,11,0.2)]">
                        {v.match_score}% Confidence
                      </span>
                    </div>
                  </div>

                  {/* Body: Side-by-side Layout */}
                  <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-8 relative">
                    {/* Official */}
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                          <CheckCircle2 className="w-3.5 h-3.5 text-green-500" /> Authorized Vault
                        </span>
                        <span className="text-xs font-mono text-slate-400">{v.official_asset}</span>
                      </div>
                      <div className="aspect-video bg-slate-900 rounded-lg overflow-hidden border border-slate-800 relative group">
                        <img src={v.official_thumb} className="w-full h-full object-cover opacity-60 group-hover:opacity-100 transition-opacity" alt="Official Frame" />
                        <div className="absolute inset-0 ring-1 ring-inset ring-white/10 rounded-lg" />
                      </div>
                    </div>

                    {/* VS divider for large screens */}
                    <div className="hidden md:flex absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-10 w-8 h-8 rounded-full bg-slate-900 border border-slate-700 items-center justify-center shadow-lg">
                      <span className="text-xs font-bold text-slate-500">VS</span>
                    </div>

                    {/* Pirated */}
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                          <Eye className="w-3.5 h-3.5 text-red-400" /> Suspect Stream
                        </span>
                        <span className="text-xs font-mono text-slate-400 truncate max-w-[120px]">{v.channel}</span>
                      </div>
                      <div className="aspect-video bg-slate-900 rounded-lg overflow-hidden border border-red-500/20 relative group">
                        <img src={v.pirated_thumb} className="w-full h-full object-cover opacity-60 group-hover:opacity-100 transition-opacity filter sepia-[0.2] contrast-125" alt="Pirated Frame" />
                        <div className="absolute inset-0 ring-1 ring-inset ring-red-500/20 rounded-lg" />
                        
                        {/* Fingerprint Match Overlay */}
                        <div className="absolute inset-0 bg-red-500/5 mix-blend-overlay">
                          <div className="absolute top-0 right-0 bottom-0 w-[2px] bg-red-400/50 blur-[2px] shadow-[0_0_10px_rgba(248,113,113,0.8)] animate-[scan_2s_ease-in-out_infinite]" />
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="px-6 py-4 border-t border-slate-800/60 bg-[#080808] flex justify-end gap-3 z-20 relative">
                    <button 
                      onClick={() => handleDismiss(v.id)}
                      className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-slate-200 transition-colors"
                    >
                      Dismiss
                    </button>
                    <button 
                      onClick={() => { setSelectedViolation(v); handleGenerateTakedown(v); }}
                      className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-medium rounded-lg transition-all shadow-lg shadow-blue-500/20 hover:shadow-blue-500/40"
                    >
                      <Gavel className="w-3.5 h-3.5" />
                      Generate Takedown
                    </button>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
            ) : activeTab === 'news' ? (
              <motion.div initial={{opacity:0}} animate={{opacity:1}} className="bg-[#0a0a0a] border border-slate-800/60 rounded-xl overflow-hidden shadow-none">
                <div className="px-6 py-4 border-b border-slate-800/60 bg-slate-900/20 flex items-center gap-2">
                   <h3 className="font-semibold text-slate-100">News Source Scanner</h3>
                </div>
                <div className="p-6">
                   <p className="text-sm text-slate-400 mb-4">Paste the raw text of a sports news article or transcript below. The AI Agent will scan it for unauthorized use of official game commentary or IP.</p>
                   <textarea 
                     value={newsText}
                     onChange={(e) => setNewsText(e.target.value)}
                     className="w-full h-48 bg-[#050505] border border-slate-700/60 rounded-lg p-4 text-sm text-slate-300 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 mb-4 font-mono leading-relaxed"
                     placeholder="Paste news text here... (optional if providing image)"
                   />
                   
                   <div className="mb-4">
                     {previewUrl ? (
                        <div className="relative inline-block border border-slate-700 rounded-lg overflow-hidden text-sm text-slate-400 bg-[#050505]">
                           <img src={previewUrl} className="h-32 object-contain bg-slate-900/50" />
                           <button onClick={removeImage} className="absolute top-1 right-1 p-1 bg-red-500 hover:bg-red-400 text-white rounded-full">
                              <X className="w-3 h-3" />
                           </button>
                        </div>
                     ) : (
                        <label className="cursor-pointer inline-flex items-center gap-2 px-4 py-2 border border-slate-700 border-dashed rounded-lg text-sm text-slate-400 hover:text-slate-200 hover:border-slate-500 transition-colors bg-[#050505]">
                          <ImageIcon className="w-4 h-4" />
                          <span>Attach Screenshot</span>
                          <input type="file" accept="image/*" className="hidden" onChange={handleImageChange} />
                        </label>
                     )}
                   </div>

                   <div className="flex justify-end border-b border-slate-800/60 pb-8 mb-8">
                     <button
                       onClick={handleScanNews}
                       disabled={isScanningNews || (!newsText.trim() && !selectedImage)}
                       className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 disabled:opacity-50 text-white px-6 py-2 rounded-lg text-xs font-bold transition-all shadow-lg"
                     >
                       {isScanningNews ? 'Scanning with Gemini...' : 'Scan Source for Infringement'}
                     </button>
                   </div>
                   
                   {/* Results Box */}
                   {newsReport && (
                     <motion.div initial={{opacity:0, y: 10}} animate={{opacity:1, y: 0}} className="bg-[#050505] border border-slate-800/60 rounded-lg p-6">
                       <div className="flex items-center gap-4 mb-4">
                         <div className={`w-14 h-14 rounded-xl flex items-center justify-center font-bold text-xl border ${newsReport.confidence_score > 0.6 ? 'bg-red-500/10 text-red-500 border-red-500/20' : 'bg-green-500/10 text-green-500 border-green-500/20'}`}>
                           {Math.round(newsReport.confidence_score * 100)}%
                         </div>
                         <div>
                           <h4 className="text-sm font-bold text-slate-200 flex items-center gap-2">
                             Classification: <span className={newsReport.confidence_score > 0.6 ? "text-red-400" : "text-green-400"}>{newsReport.classification}</span>
                           </h4>
                           <p className="text-xs text-slate-500 mt-1">Source Credibility: <strong>{newsReport.source_credibility}</strong></p>
                         </div>
                       </div>
                       
                       <div className="flex gap-2 mb-6">
                         {newsReport.misappropriation_detected && <span className="px-2 py-1 bg-amber-500/10 text-amber-500 border border-amber-500/20 text-[10px] font-bold uppercase rounded flex items-center gap-1"><AlertTriangle className="w-3 h-3"/> Misappropriation</span>}
                         {newsReport.anomaly_detected && <span className="px-2 py-1 bg-purple-500/10 text-purple-400 border border-purple-500/20 text-[10px] font-bold uppercase rounded flex items-center gap-1"><AlertTriangle className="w-3 h-3"/> Viral Anomaly</span>}
                         {!newsReport.misappropriation_detected && !newsReport.anomaly_detected && <span className="px-2 py-1 bg-green-500/10 text-green-500 border border-green-500/20 text-[10px] font-bold uppercase rounded flex items-center gap-1"><CheckCircle2 className="w-3 h-3"/> Origin Verified</span>}
                       </div>
                       
                       <div className="space-y-6 text-sm">
                         <div className="bg-slate-900/40 p-4 rounded-lg border border-slate-800/60">
                           <span className="text-[10px] uppercase tracking-wider text-slate-500 font-bold block mb-2">AI Explanation</span>
                           <p className="text-slate-300 leading-relaxed">{newsReport.explanation}</p>
                         </div>
                         
                         {newsReport.key_flags && newsReport.key_flags.length > 0 && (
                           <div>
                             <span className="text-[10px] uppercase tracking-wider text-amber-500/70 font-bold block mb-2 flex items-center gap-2"><AlertTriangle className="w-3 h-3"/> Key Flags Identified</span>
                             <ul className="list-disc list-inside space-y-2">
                               {newsReport.key_flags.map((flag: string, i: number) => (
                                 <li key={i} className="text-amber-100/80 italic text-xs marker:text-amber-500 pl-2">{flag}</li>
                               ))}
                             </ul>
                           </div>
                         )}
                         
                         {newsReport.takedown_letter_draft && newsReport.confidence_score > 0.6 && (
                           <div>
                             <span className="text-[10px] uppercase tracking-wider text-red-400 font-bold block mb-2 flex items-center gap-2"><Gavel className="w-3 h-3"/> Warning Letter Drafted</span>
                             <pre className="whitespace-pre-wrap font-mono text-[10px] text-slate-400 leading-relaxed bg-[#0a0a0a] p-4 rounded border border-red-900/40 max-h-48 overflow-y-auto mb-3">
                               {newsReport.takedown_letter_draft}
                             </pre>
                             <div className="flex justify-end">
                                <button
                                  onClick={() => {
                                     setTakedownQueue(prev => [{
                                        id: `FAKE_NEWS_${Date.now()}`,
                                        notice: newsReport.takedown_letter_draft,
                                        violation: { channel: 'Pasted News Source' }
                                     }, ...prev]);
                                     setNewsReport(null);
                                     setActiveTab('queue');
                                  }}
                                  className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-red-600 to-amber-600 hover:from-red-500 hover:to-amber-500 text-white text-xs font-medium rounded-lg transition-all shadow-lg"
                                >
                                  <Send className="w-3.5 h-3.5" />
                                  Push Draft to Queue
                                </button>
                             </div>
                           </div>
                         )}
                       </div>
                     </motion.div>
                   )}
                </div>
              </motion.div>
            ) : activeTab === 'fingerprints' ? (
              <motion.div initial={{opacity:0}} animate={{opacity:1}} className="bg-[#0a0a0a] border border-slate-800/60 rounded-xl overflow-hidden shadow-none">
                <div className="px-6 py-4 border-b border-slate-800/60 bg-slate-900/20 flex items-center gap-2">
                   <h3 className="font-semibold text-slate-100">Asset Fingerprint Vault</h3>
                </div>
                <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-8">
                   
                   <div>
                     <h4 className="text-sm font-bold text-slate-200 mb-4">Ingest Official Asset</h4>
                     <p className="text-xs text-slate-400 mb-6">Upload an official broadcast MP4. The system will extract keyframes, generate hashes, and deposit them into the local ChromaDB vector vault for real-time comparison against pirated streams.</p>
                     
                     <div className="space-y-4">
                       <div>
                         <label className="block text-xs uppercase text-slate-500 font-bold mb-1">Asset Reference ID</label>
                         <input 
                           type="text" 
                           value={fingerprintVideoId}
                           onChange={(e) => setFingerprintVideoId(e.target.value)}
                           className="w-full bg-[#050505] border border-slate-700/60 rounded-lg p-2.5 text-sm text-slate-300 focus:outline-none focus:border-indigo-500"
                           placeholder="e.g. LAL_MIA_03192026_CAM2"
                         />
                       </div>
                       
                       <div>
                         <label className="block text-xs uppercase text-slate-500 font-bold mb-1">Video File</label>
                         <label className="cursor-pointer flex flex-col items-center justify-center border-2 border-slate-700 border-dashed rounded-lg p-6 text-slate-400 hover:text-slate-200 hover:border-slate-500 transition-colors bg-[#050505]">
                           <UploadCloud className="w-8 h-8 mb-2 opacity-50" />
                           <span className="text-sm font-medium">{fingerprintFile ? fingerprintFile.name : 'Drag & Drop or Click to Select MP4'}</span>
                           <input type="file" accept="video/mp4,video/x-m4v,video/*" className="hidden" onChange={handleFingerprintFileChange} />
                         </label>
                       </div>
                       
                       <button
                         onClick={handleUploadAsset}
                         disabled={isUploadingAsset || !fingerprintFile || !fingerprintVideoId.trim()}
                         className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white px-4 py-3 rounded-lg text-sm font-bold transition-all shadow-lg flex items-center justify-center gap-2"
                       >
                         {isUploadingAsset ? (
                           <>Extracting Keyframes & Hashing...</>
                         ) : (
                           <><Shield className="w-4 h-4"/> Deposit to ChromaDB Vault</>
                         )}
                       </button>
                     </div>
                   </div>

                   <div className="border-t lg:border-t-0 lg:border-l border-slate-800/60 pt-6 lg:pt-0 lg:pl-8">
                     <h4 className="text-sm font-bold text-slate-200 mb-4">Indexed Assets Database</h4>
                     <div className="space-y-3">
                       {indexedAssets.map((asset, i) => (
                         <div key={i} className="bg-[#050505] border border-slate-800/60 rounded-lg p-3 flex items-center justify-between">
                           <div className="flex items-center gap-3">
                             <div className="w-8 h-8 rounded-full bg-green-500/10 flex items-center justify-center">
                               <CheckCircle2 className="w-4 h-4 text-green-500" />
                             </div>
                             <div>
                               <p className="text-xs font-bold text-slate-200">{asset.id}</p>
                               <p className="text-[10px] text-slate-500 truncate max-w-[150px]">{asset.name}</p>
                             </div>
                           </div>
                           <span className="text-[10px] font-mono text-slate-600">ACTIVE</span>
                         </div>
                       ))}
                     </div>
                   </div>

                </div>
              </motion.div>
            ) : activeTab === 'queue' ? (
              <motion.div initial={{opacity:0}} animate={{opacity:1}} className="bg-[#0a0a0a] border border-slate-800/60 rounded-xl overflow-hidden shadow-none">
                <div className="px-6 py-4 border-b border-slate-800/60 bg-slate-900/20 flex items-center justify-between">
                   <h3 className="font-semibold text-slate-100 flex items-center gap-2"><Gavel className="w-5 h-5 text-indigo-400"/> Takedown Queue</h3>
                   <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                     {takedownQueue.length} PENDING
                   </span>
                </div>
                
                {takedownQueue.length === 0 ? (
                  <div className="p-12 flex flex-col items-center justify-center text-slate-500 min-h-[300px]">
                     <CheckCircle2 className="w-12 h-12 mb-4 opacity-30 text-green-500" />
                     <p className="text-lg font-medium text-slate-300 mb-2">Queue is Empty</p>
                     <p className="text-sm text-center max-w-md">No pending DMCA drafts. Navigate to the Live Feed to generate takedowns for active violations.</p>
                  </div>
                ) : (
                  <div className="p-6 space-y-4">
                    {takedownQueue.map((item) => (
                      <div key={item.id} className="bg-[#050505] border border-slate-800 rounded-lg p-5 group flex flex-col md:flex-row gap-6">
                        <div className="flex-1 space-y-3">
                           <div className="flex items-start justify-between">
                             <div>
                               <span className="text-[10px] uppercase tracking-wider text-slate-500 font-bold">Target Instance</span>
                               <p className="text-sm font-bold text-red-400">{item.id} — {item.violation.channel}</p>
                             </div>
                             <span className="text-xs font-mono text-slate-400 bg-slate-800/50 px-2 py-1 rounded">DRAFTED</span>
                           </div>
                           <pre className="whitespace-pre-wrap font-mono text-[10px] text-slate-400 leading-relaxed bg-[#0a0a0a] p-3 rounded border border-slate-800 max-h-32 overflow-y-auto">
                             {item.notice}
                           </pre>
                        </div>
                        <div className="flex md:flex-col items-end justify-end gap-3 md:min-w-[160px]">
                           <button 
                             onClick={() => handleTransmitToISP(item.id)}
                             className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-white hover:bg-slate-200 text-slate-900 text-xs font-bold rounded-lg transition-colors shadow-lg"
                           >
                             <Send className="w-4 h-4"/> 
                             Transmit
                           </button>
                           <button 
                             onClick={() => handleTransmitToISP(item.id)}
                             className="w-full px-4 py-2 text-xs font-medium text-slate-500 hover:text-red-400 transition-colors"
                           >
                             Discard Draft
                           </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </motion.div>
            ) : (
              <div className="bg-[#0a0a0a] border border-slate-800/60 p-12 flex flex-col items-center justify-center rounded-xl text-slate-500 min-h-[400px]">
                 <Terminal className="w-12 h-12 mb-4 opacity-30" />
                 <p className="text-lg font-medium text-slate-300 mb-2">Agent System Logs</p>
                 <p className="text-sm text-center max-w-md">Live agent stdout monitoring will be available here.</p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Takedown Modal Overlay */}
      <AnimatePresence>
        {selectedViolation && (
          <motion.div 
            initial={{ opacity: 0 }} 
            animate={{ opacity: 1 }} 
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
          >
            <motion.div 
              initial={{ scale: 0.95, opacity: 0, y: 20 }} 
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.95, opacity: 0, y: 20 }}
              className="w-full max-w-2xl bg-[#0a0a0a] border border-slate-700/60 rounded-xl overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.8)] flex flex-col max-h-[90vh]"
            >
              <div className="px-6 py-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
                <div className="flex items-center gap-2">
                  <Gavel className="w-5 h-5 text-indigo-400" />
                  <h3 className="font-semibold text-slate-100">AI Takedown Drafter</h3>
                </div>
                <button onClick={closeTakedownDraft} className="text-slate-500 hover:text-slate-300">
                  <X className="w-5 h-5" />
                </button>
              </div>
              
              <div className="p-6 overflow-auto bg-[#050505]">
                {isDrafting ? (
                  <div className="flex flex-col items-center justify-center py-12 space-y-4">
                    <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
                    <p className="text-sm font-medium text-slate-400 animate-pulse">Gemini 1.5 is analyzing reasoning and drafting notice...</p>
                  </div>
                ) : (
                  <motion.div 
                    initial={{ opacity: 0 }} 
                    animate={{ opacity: 1 }}
                    className="relative"
                  >
                    <div className="absolute top-2 right-2 flex gap-2">
                      <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                        Drafted by Gemini
                      </span>
                    </div>
                    <pre className="whitespace-pre-wrap font-mono text-xs text-slate-300 leading-relaxed bg-slate-900/50 p-6 rounded-lg border border-slate-800">
                      {takedownDraft}
                    </pre>
                  </motion.div>
                )}
              </div>
              
              {!isDrafting && (
                <div className="px-6 py-4 border-t border-slate-800 bg-[#0a0a0a] flex justify-end gap-3">
                  <button onClick={closeTakedownDraft} className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-slate-200">
                    Cancel
                  </button>
                  <button 
                    onClick={handleSendNotice}
                    className="flex items-center gap-2 px-6 py-2 bg-white hover:bg-slate-100 text-slate-900 text-xs font-bold rounded-lg transition-colors"
                  >
                    Send Notice
                  </button>
                </div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <style dangerouslySetInnerHTML={{__html: `
        @keyframes scan {
          0% { transform: translateX(0%); opacity: 0; }
          10% { opacity: 1; }
          90% { opacity: 1; }
          100% { transform: translateX(400px); opacity: 0; }
        }
      `}} />
    </div>
  );
}

function SidebarItem({ children, icon, active, onClick }: { children: React.ReactNode; icon: React.ReactNode; active?: boolean; onClick?: () => void }) {
  return (
    <button onClick={onClick} className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all text-sm ${active ? 'bg-blue-600/10 text-blue-400 font-medium border border-blue-500/20 shadow-[inset_0_1px_0_rgba(255,255,255,0.05)]' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'}`}>
      <span className={active ? "text-blue-400" : "text-slate-500"}>{icon}</span>
      {children}
    </button>
  );
}
