import React, { useState } from 'react';

export default function HomePage() {
    const [dragActive, setDragActive] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
        setDragActive(true);
        } else if (e.type === "dragleave") {
        setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        setSelectedFile(e.dataTransfer.files[0]);
        }
    };

    const handleFileSelect = (e) => {
        if (e.target.files && e.target.files[0]) {
        setSelectedFile(e.target.files[0]);
        }
    };

    const handleAnalyze = () => {
        if (selectedFile) {
        alert(`Analyzing card: ${selectedFile.name}`);
        // Add your analysis logic here
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                <div className="w-6 h-6 border-2 border-gray-800 rounded-full flex items-center justify-center">
                    <div className="w-2 h-2 bg-gray-800 rounded-full"></div>
                </div>
                <h1 className="text-xl font-serif tracking-wide">PIERCE & PIERCE</h1>
                </div>
                <nav className="flex items-center space-x-8">
                <a href="#" className="text-sm font-medium text-gray-700 hover:text-gray-900">HOME</a>
                <a href="#" className="text-sm font-medium text-gray-700 hover:text-gray-900">HISTORY</a>
                <a href="#" className="text-sm font-medium text-gray-700 hover:text-gray-900">CONTACT</a>
                <button className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center hover:bg-gray-200">
                    <svg className="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                </button>
                </nav>
            </div>
            </div>
        </header>

        {/* Main Content */}
        <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
            <div className="text-center mb-12">
            <h2 className="text-4xl font-serif text-gray-900 mb-4">Business Card Analysis</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
                Show me your card… if you have the confidence.
            </p>
            </div>

            {/* Upload Area */}
            <div
            className={`bg-gray-100 border-2 border-dashed rounded-lg p-16 mb-8 transition-colors ${
                dragActive ? 'border-gray-400 bg-gray-200' : 'border-gray-300'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            >
            <div className="text-center">
                <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Drag & Drop Your Card Here</h3>
                <p className="text-sm text-gray-500 mb-4">or, if you must, click to browse</p>
                
                <label htmlFor="file-upload">
                <input
                    id="file-upload"
                    type="file"
                    className="hidden"
                    accept="image/*"
                    onChange={handleFileSelect}
                />
                <span className="inline-block px-6 py-2 border border-gray-300 rounded bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 cursor-pointer">
                    SELECT FILE
                </span>
                </label>
                
                {selectedFile && (
                <p className="mt-4 text-sm text-gray-600">
                    Selected: <span className="font-medium">{selectedFile.name}</span>
                </p>
                )}
            </div>
            </div>

            {/* Analyze Button */}
            <div className="text-center">
            <button
                onClick={handleAnalyze}
                disabled={!selectedFile}
                className={`px-12 py-3 rounded text-white font-medium text-sm tracking-wide transition-colors ${
                selectedFile
                    ? 'bg-red-800 hover:bg-red-900'
                    : 'bg-gray-400 cursor-not-allowed'
                }`}
            >
                ANALYZE CARD
            </button>
            </div>
        </main>

        {/* Footer */}
        <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 mt-16 border-t border-gray-200">
            <div className="flex justify-center space-x-8 mb-4">
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">About Us</a>
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">Privacy Policy</a>
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">Terms of Service</a>
            </div>
            <p className="text-center text-xs text-gray-500">
            © 2024 Pierce & Pierce. All Rights Reserved.
            </p>
        </footer>
        </div>
    );
}