import { MoonIcon, SunIcon } from "lucide-react";
import { useTheme } from "next-themes";
import { Button } from "../ui/button";

const ModeToggle = () => {
  const { theme, setTheme } = useTheme();

  return (
    <Button variant={"ghost"} onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
      {theme === "dark" ? <SunIcon /> : <MoonIcon />}
    </Button>
  );
};

export default ModeToggle;
