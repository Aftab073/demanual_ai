import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiArrowRight, FiZap, FiTrendingUp } from 'react-icons/fi';
import { FaLinkedin } from 'react-icons/fa';

const trendingTopics = [
  'Artificial Intelligence',
  'Quantum Computing',
  'Sustainable Technology',
  'Blockchain',
  'Cybersecurity',
  'Machine Learning'
];

function HomePage() {
  const [topic, setTopic] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const navigate = useNavigate();

  const handleGenerateClick = () => {
    if (!topic.trim()) {
      alert('Please enter a topic.');
      return;
    }
    navigate(`/result?topic=${encodeURIComponent(topic)}`);
  };

  const handleTrendingClick = (trendingTopic) => {
    setTopic(trendingTopic);
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] relative overflow-hidden">
      {/* LinkedIn Blue Light Beam - Dramatic and Professional */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[2px] h-[55vh] opacity-80 pointer-events-none z-0">
        {/* Outer blue glow */}
        <motion.div
          className="absolute top-0 left-1/2 -translate-x-1/2 w-[250px] h-full"
          style={{
            background: 'linear-gradient(180deg, rgba(10, 102, 194, 0.2) 0%, rgba(10, 102, 194, 0.4) 50%, rgba(56, 152, 236, 0.6) 100%)',
            filter: 'blur(60px)',
          }}
          animate={{
            opacity: [0.4, 0.7, 0.4],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        
        {/* Middle glow */}
        <motion.div
          className="absolute top-0 left-1/2 -translate-x-1/2 w-[100px] h-full"
          style={{
            background: 'linear-gradient(180deg, rgba(56, 152, 236, 0.5) 0%, rgba(10, 102, 194, 0.8) 50%, rgba(56, 152, 236, 1) 100%)',
            filter: 'blur(30px)',
          }}
          animate={{
            opacity: [0.6, 1, 0.6],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />

        {/* Core beam */}
        <div 
          className="absolute top-0 left-1/2 -translate-x-1/2 w-[2px] h-full bg-gradient-to-b from-white via-blue-300 to-blue-500"
          style={{
            boxShadow: '0 0 30px 15px rgba(56, 152, 236, 0.6)',
          }}
        />

        {/* Falling particle effect */}
        <motion.div
          className="absolute top-0 left-1/2 -translate-x-1/2 w-1 h-20 bg-gradient-to-b from-white to-transparent"
          animate={{
            top: ["0%", "100%"],
            opacity: [1, 0],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "linear"
          }}
        />
      </div>

      {/* Radial blue glow at top */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[300px]">
        <div 
          className="w-full h-full"
          style={{
            background: 'radial-gradient(circle, rgba(10, 102, 194, 0.4) 0%, transparent 70%)',
            filter: 'blur(100px)',
          }}
        />
      </div>

      {/* Main Content */}
      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Logo/Brand */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="flex items-center justify-center space-x-3 mb-8"
        >
          <FaLinkedin className="text-3xl text-[#0A66C2]" />
          <span className="text-xl font-bold text-white">PostGenius AI</span>
        </motion.div>

        {/* CENTERED Hero Section */}
        <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
            className="text-center space-y-6 max-w-4xl"
          >
            {/* Main Heading */}
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-white leading-tight">
              Transform Topics Into
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#0A66C2] via-blue-400 to-[#0A66C2]">
                Viral LinkedIn Posts
              </span>
            </h1>

            {/* Subheading */}
            <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto">
              AI-powered content generation backed by real-time news analysis
            </p>

            {/* INPUT BOX with LinkedIn blue theme */}
            <div className="relative mt-10">
              {/* Blue glow pool */}
              <div 
                className="absolute -inset-8 rounded-full pointer-events-none"
                style={{
                  background: 'radial-gradient(circle, rgba(10, 102, 194, 0.15) 0%, transparent 70%)',
                  filter: 'blur(40px)',
                }}
              />

              <div className="relative max-w-2xl mx-auto space-y-4">
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  onFocus={() => setIsFocused(true)}
                  onBlur={() => setIsFocused(false)}
                  placeholder="Enter your topic..."
                  onKeyPress={(e) => e.key === 'Enter' && handleGenerateClick()}
                  className="w-full bg-white/5 backdrop-blur-sm border border-white/20 rounded-2xl px-8 py-6 text-white placeholder-gray-500 text-lg focus:outline-none transition-all"
                  style={{
                    borderColor: isFocused ? 'rgba(10, 102, 194, 0.5)' : 'rgba(255, 255, 255, 0.2)',
                    boxShadow: isFocused 
                      ? '0 0 30px rgba(10, 102, 194, 0.3), inset 0 2px 20px rgba(10, 102, 194, 0.1)' 
                      : '0 0 15px rgba(10, 102, 194, 0.15)',
                  }}
                />

                {/* LinkedIn Blue Generate Button */}
                <motion.button
                  onClick={handleGenerateClick}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full bg-gradient-to-r from-[#0A66C2] to-blue-500 text-white font-bold py-5 px-8 rounded-2xl flex items-center justify-center space-x-2 shadow-2xl shadow-blue-500/30 hover:shadow-blue-500/50 transition-all group"
                >
                  <FiZap className="text-xl" />
                  <span className="text-lg">Generate Post</span>
                  <FiArrowRight className="text-xl group-hover:translate-x-1 transition-transform" />
                </motion.button>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Feature Cards - Reduced margin */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto mt-8"
        >
          {[
            {
              title: 'AI-Powered',
              desc: 'Advanced algorithms analyze trends',
              icon: '🤖'
            },
            {
              title: 'Real-Time Data',
              desc: 'Latest news and insights',
              icon: '⚡'
            },
            {
              title: 'Instant Results',
              desc: 'Professional posts in seconds',
              icon: '🚀'
            }
          ].map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 + index * 0.1 }}
              className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 text-center hover:bg-white/10 hover:border-blue-500/30 transition-all group"
            >
              <div className="text-4xl mb-3">{feature.icon}</div>
              <h3 className="text-lg font-bold text-white mb-2 group-hover:text-[#0A66C2] transition-colors">
                {feature.title}
              </h3>
              <p className="text-gray-400 text-sm">{feature.desc}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* Trending Topics - Reduced margin, now visible */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="max-w-4xl mx-auto mt-10 space-y-4 pb-8"
        >
          <div className="flex items-center justify-center space-x-2 text-gray-400">
            <FiTrendingUp className="text-[#0A66C2]" />
            <span className="text-sm font-medium">Trending Topics</span>
          </div>
          <div className="flex flex-wrap gap-3 justify-center">
            {trendingTopics.map((trendingTopic, index) => (
              <motion.button
                key={index}
                onClick={() => handleTrendingClick(trendingTopic)}
                whileHover={{ scale: 1.05, backgroundColor: 'rgba(10, 102, 194, 0.15)' }}
                whileTap={{ scale: 0.95 }}
                className="px-5 py-2.5 bg-white/5 border border-white/10 rounded-full text-sm text-gray-300 hover:text-[#0A66C2] hover:border-blue-500/50 transition-all"
              >
                {trendingTopic}
              </motion.button>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}

export default HomePage;
