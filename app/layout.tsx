import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "Nova Academy | Pilot Registration", description: "Your next chapter is out there. Start at the Nova Academy gate." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
