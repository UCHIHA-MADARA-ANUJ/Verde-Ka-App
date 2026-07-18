"use client";
// Smooth spring-animated number — every stat ticks like an instrument.
import { useEffect, useRef } from "react";
import {
  motion,
  useSpring,
  useTransform,
  useMotionValue,
} from "framer-motion";

export default function AnimatedNumber({ value, decimals = 0, className }) {
  const mv = useMotionValue(0);
  const spring = useSpring(mv, { stiffness: 80, damping: 20, mass: 0.6 });
  const display = useTransform(spring, (v) => v.toFixed(decimals));
  const first = useRef(true);

  useEffect(() => {
    if (first.current) {
      first.current = false;
      // small delay so entry animations land first
      const t = setTimeout(() => mv.set(Number(value) || 0), 250);
      return () => clearTimeout(t);
    }
    mv.set(Number(value) || 0);
  }, [value, mv]);

  return <motion.span className={className}>{display}</motion.span>;
}
