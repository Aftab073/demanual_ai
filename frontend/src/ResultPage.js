import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiArrowLeft, FiCopy, FiCheck, FiThumbsUp, FiThumbsDown, FiExternalLink } from 'react-icons/fi';
import { FaLinkedin } from 'react-icons/fa';
import toast, { Toaster } from 'react-hot-toast';

function ResultPage() {
  const [searchParams] = useSearchParams();
  const topic = searchParams.get('topic');

  const [agentResponse, setAgentResponse] = useState({ steps: [], finalAnswer: '', sources: [] });
  const [isStreaming, setIsStreaming] = useState(false);
  const [copied, setCopied] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentStage, setCurrentStage] = useState('');
  const fetchInitiated = useRef(false);

  const stages = ['Searching', 'Analyzing', 'Writing'];

  useEffect(() => {
    if (!topic || fetchInitiated.current) return;
    fetchInitiated.current = true;

    const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';


    const handleGenerate = async () => {
      setAgentResponse({ steps: [], finalAnswer: '', sources: [] });
      setIsStreaming(true);
      setProgress(0);
      setCurrentStage('Searching');

      try {
        const url = `${API_URL}/generate-post-stream?topic=${encodeURIComponent(topic)}`;
        const response = await fetch(url);

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const parts = buffer.split('\n\n');
          buffer = parts.pop();

          for (const part of parts) {
            if (part.startsWith('data: ')) {
              const dataString = part.substring(6);

              if (dataString === '[DONE]') {
                setIsStreaming(false);
                setProgress(100);
                setCurrentStage('Complete');
                return;
              }

              try {
                const chunk = JSON.parse(dataString);

                if (chunk.type === 'action') {
                  const stepText = `🔍 ${chunk.tool}: ${chunk.tool_input}`;
                  setAgentResponse(prev => ({ ...prev, steps: [...prev.steps, stepText] }));
                  setProgress(33);
                  setCurrentStage('Searching');
                } else if (chunk.type === 'observation') {
                  const stepText = `📊 Found: ${chunk.observation.substring(0, 100)}...`;
                  setAgentResponse(prev => ({ ...prev, steps: [...prev.steps, stepText] }));
                  setProgress(66);
                  setCurrentStage('Analyzing');
                } else if (chunk.type === 'output') {
                  setAgentResponse(prev => ({ ...prev, finalAnswer: chunk.output }));
                  setProgress(100);
                  setCurrentStage('Writing');
                } else if (chunk.type === 'sources') {
                  setAgentResponse(prev => ({ ...prev, sources: chunk.sources }));
                }
              } catch (e) {
                console.error("Failed to parse JSON chunk:", dataString, e);
              }
            }
          }
        }
      } catch (error) {
        console.error("Fetch stream failed:", error);
        toast.error('Failed to generate post. Please try again.');
      } finally {
        setIsStreaming(false);
      }
    };

    handleGenerate();
  }, [topic]);

  const handleCopy = () => {
    navigator.clipboard.writeText(agentResponse.finalAnswer);
    setCopied(true);
    toast.success('Copied to clipboard!');
    setTimeout(() => setCopied(false), 2000);
  };

  const handleFeedback = (type) => {
    toast.success(`Thanks for your ${type === 'like' ? '👍' : '👎'} feedback!`);
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] relative overflow-hidden">
      <Toaster position="top-center" />

      {/* Dynamic Light Beam */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[2px] h-full pointer-events-none z-0">
        <motion.div
          className="absolute top-0 left-1/2 -translate-x-1/2 w-[200px] h-full"
          style={{
            background: 'linear-gradient(180deg, rgba(10, 102, 194, 0.3) 0%, rgba(56, 152, 236, 0.5) 50%, rgba(10, 102, 194, 0.3) 100%)',
            filter: 'blur(50px)',
          }}
          animate={{
            opacity: isStreaming ? [0.5, 0.9, 0.5] : 0.3,
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />

        <motion.div
          className="absolute top-0 left-1/2 -translate-x-1/2 w-[2px] h-full bg-gradient-to-b from-transparent via-blue-400 to-transparent"
          animate={{
            opacity: isStreaming ? [0.7, 1, 0.7] : 0.5,
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
          }}
        />
      </div>

      {/* Main Content */}
      <div className="relative z-10 container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Link to="/">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors"
            >
              <FiArrowLeft />
              <span>Back</span>
            </motion.button>
          </Link>

          <div className="flex items-center space-x-2">
            <FaLinkedin className="text-2xl text-[#0A66C2]" />
            <span className="text-white font-semibold">PostGenius AI</span>
          </div>
        </div>

        {/* Topic Display */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
            Generating Post About
          </h1>
          <p className="text-xl text-[#0A66C2]">"{topic}"</p>
        </motion.div>

        {/* Progress Bar */}
        {isStreaming && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mb-8"
          >
            <div className="flex justify-between items-center mb-3">
              {stages.map((stage, index) => (
                <div key={stage} className="flex items-center">
                  <div className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${currentStage === stage
                      ? 'bg-[#0A66C2] text-white'
                      : progress > (index * 33)
                        ? 'bg-blue-900/50 text-blue-300'
                        : 'bg-white/5 text-gray-500'
                    }`}>
                    {stage}
                  </div>
                  {index < stages.length - 1 && (
                    <div className="w-12 h-0.5 bg-white/10 mx-2" />
                  )}
                </div>
              ))}
            </div>

            <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-[#0A66C2] to-blue-400"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
          </motion.div>
        )}

        {/* Agent's Thought Process */}
        {agentResponse.steps.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6 mb-6"
          >
            <h2 className="text-xl font-bold text-white mb-4 flex items-center">
              <span className="mr-2">🧠</span> AI Thought Process
            </h2>
            <div className="space-y-3">
              {agentResponse.steps.map((step, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="text-gray-300 text-sm bg-white/5 rounded-lg p-3"
                >
                  {step}
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Final Generated Post */}
        {agentResponse.finalAnswer && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 mb-6"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white flex items-center">
                <span className="mr-2">✨</span> Your LinkedIn Post
              </h2>

              <motion.button
                onClick={handleCopy}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center space-x-2 bg-[#0A66C2] text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
              >
                {copied ? <FiCheck /> : <FiCopy />}
                <span>{copied ? 'Copied!' : 'Copy'}</span>
              </motion.button>
            </div>

            <div className="text-gray-200 whitespace-pre-wrap leading-relaxed mb-6">
              {agentResponse.finalAnswer}
            </div>

            {/* Feedback Buttons */}
            <div className="flex items-center justify-center space-x-4 pt-4 border-t border-white/10">
              <span className="text-gray-400 text-sm">Was this helpful?</span>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => handleFeedback('like')}
                className="p-2 bg-white/5 rounded-full hover:bg-green-500/20 hover:text-green-400 transition-colors"
              >
                <FiThumbsUp />
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => handleFeedback('dislike')}
                className="p-2 bg-white/5 rounded-full hover:bg-red-500/20 hover:text-red-400 transition-colors"
              >
                <FiThumbsDown />
              </motion.button>
            </div>
          </motion.div>
        )}

        {/* News Sources Section */}
        {agentResponse.sources.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6"
          >
            <h3 className="text-xl font-bold text-white mb-4 flex items-center">
              <span className="mr-2">📰</span> News Sources
            </h3>
            <div className="space-y-3">
              {agentResponse.sources.map((source, index) => (
                <motion.a
                  key={index}
                  href={source.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.02, backgroundColor: 'rgba(10, 102, 194, 0.1)' }}
                  className="flex items-start space-x-3 p-4 bg-white/5 rounded-xl hover:border-[#0A66C2] border border-transparent transition-all group"
                >
                  <div className="flex-1">
                    <p className="text-gray-200 font-medium group-hover:text-[#0A66C2] transition-colors">
                      {source.title}
                    </p>
                    <p className="text-gray-500 text-sm mt-1 truncate">{source.link}</p>
                  </div>
                  <FiExternalLink className="text-gray-400 group-hover:text-[#0A66C2] transition-colors flex-shrink-0 mt-1" />
                </motion.a>
              ))}
            </div>
          </motion.div>
        )}

        {/* Loading State */}
        {isStreaming && agentResponse.steps.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#0A66C2] mb-4"></div>
            <p className="text-gray-400">Connecting to AI agent...</p>
          </motion.div>
        )}
      </div>
    </div>
  );
}

export default ResultPage;
