/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
    "./lib/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        verde: {
          bg: "#0c0c0c",
          panel: "#121212",
          card: "#161b16",
          border: "#1f2a1f",
          green: "#22c55e",
          dim: "#15803d",
          text: "#d1fae5",
          muted: "#6b7280",
          danger: "#ef4444",
          water: "#38bdf8",
        },
      },
      fontFamily: {
        mono: [
          "'Share Tech Mono'",
          "'Courier Prime'",
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "monospace",
        ],
      },
      boxShadow: {
        "glow-sm": "0 0 8px rgba(34,197,94,0.25)",
        glow: "0 0 15px rgba(34,197,94,0.3)",
        "glow-lg": "0 0 25px rgba(34,197,94,0.45)",
        "glow-red": "0 0 15px rgba(239,68,68,0.4)",
        "glow-water": "0 0 15px rgba(56,189,248,0.35)",
      },
      keyframes: {
        "pulse-red": {
          "0%, 100%": { boxShadow: "0 0 8px rgba(239,68,68,0.3)" },
          "50%": { boxShadow: "0 0 22px rgba(239,68,68,0.7)" },
        },
        scanline: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100%)" },
        },
        blink: {
          "0%, 100%": { opacity: 1 },
          "50%": { opacity: 0 },
        },
      },
      animation: {
        "pulse-red": "pulse-red 1.2s ease-in-out infinite",
        scanline: "scanline 6s linear infinite",
        blink: "blink 1s step-start infinite",
      },
    },
  },
  plugins: [],
};
