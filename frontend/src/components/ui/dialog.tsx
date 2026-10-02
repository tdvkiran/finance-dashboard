// Placeholder for dialog to keep it simple, shadcn dialog is complex
import * as React from "react"

export const Dialog = ({ children }: any) => <div>{children}</div>
export const DialogTrigger = ({ children }: any) => <>{children}</>
export const DialogContent = ({ children }: any) => <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80">{children}</div>
export const DialogHeader = ({ children }: any) => <div>{children}</div>
export const DialogTitle = ({ children }: any) => <h2>{children}</h2>
