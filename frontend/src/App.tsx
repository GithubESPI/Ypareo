import { ThemeProvider } from "next-themes";
import Dropzone from "./components/shared/Dropzone";
import Hero from "./components/shared/Hero";
import Navbar from "./components/shared/Navbar";

const App = () => {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem themes={["light", "dark"]}>
      <main>
        <Navbar />
        <div className="pt-32 min-h-screen lg:pt-36 2xl:pt-44 container max-w-4xl lg:max-w-6xl 2xl:max-w-7xl">
          <Hero />
          <Dropzone />
        </div>
      </main>
    </ThemeProvider>
  );
};

export default App;
