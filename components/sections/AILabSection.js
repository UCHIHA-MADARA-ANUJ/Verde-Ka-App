"use client";
// ═══ SECTION: AI LAB — camera + AI diagnostics, full width ═══
import AIDeck from "@/components/AIDeck";
import { motion } from "framer-motion";
import { Camera, Cpu, MessageSquareText } from "lucide-react";

const PIPELINE = [
  {
    icon: Camera,
    step: "01 · CAPTURE",
    body: "ESP32-CAM wakes on your command, fires its flash, and snaps an 800×600 SVGA frame of the foliage.",
  },
  {
    icon: Cpu,
    step: "02 · IDENTIFY",
    body: "Plant.id neural nets identify the species and score disease probability across leaf-pathogen classes.",
  },
  {
    icon: MessageSquareText,
    step: "03 · PRESCRIBE",
    body: "Gemini 2.0 Flash converts the diagnosis into a friendly organic treatment plan, printed in the terminal.",
  },
];

export default function AILabSection({ controls, requestCapture, scan, online }) {
  return (
    <div className="space-y-5">
      {/* Pipeline explainer */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {PIPELINE.map((p, i) => {
          const Icon = p.icon;
          return (
            <motion.div
              key={p.step}
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
              className="crt relative rounded-lg border border-verde-border bg-verde-card p-4"
            >
              <div className="mb-2 flex items-center gap-2 text-verde-green">
                <Icon size={14} />
                <p className="text-[10px] tracking-widest">{p.step}</p>
              </div>
              <p className="text-[10px] leading-relaxed text-verde-dim">
                {p.body}
              </p>
            </motion.div>
          );
        })}
      </div>

      <AIDeck
        controls={controls}
        requestCapture={requestCapture}
        scan={scan}
        online={online}
      />
    </div>
  );
}
