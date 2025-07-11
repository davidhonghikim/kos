export const EnvOverlay = () => (
  <div className="fixed bottom-0 left-0 bg-black text-white p-2 text-xs opacity-70 z-50">
    ENV: {process.env.NODE_ENV} | API: {process.env.NEXT_PUBLIC_API_HOST}
  </div>
) 