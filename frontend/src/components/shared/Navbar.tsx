import { Menu } from "lucide-react";
import { Button } from "../ui/button";
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTrigger } from "../ui/sheet";
import ModeToggle from "./mode-toogle";
import logo from "/assets/logo.png";

const Navbar = () => {
  return (
    <nav className="w-full backdrop-blur-md bg-background bg-opacity-30 z-50 fixed h-24 flex justify-between items-center py-10 px-4 md:px-8 lg:px-12 xl:px-16 2xl:px-24">
      <a href="/">
        <img src={logo} className="cursor-pointer w-40 dark:invert" alt="" />
      </a>
      <div className="gap-1 md:gap-2 lg:gap-4 hidden md:flex">
        <Button variant="ghost" className="font-semibold text-md">
          <a href="/">Accueil</a>
        </Button>
        <a href="/about">
          <Button variant="ghost" className="font-semibold text-md">
            À propos
          </Button>
        </a>
        <a href="/privacy-policy">
          <Button variant="ghost" className="font-semibold text-md">
            Confidentialité
          </Button>
        </a>
      </div>

      <div className="hidden md:flex items-center gap-2">
        <ModeToggle />
        <a href="/">
          <Button
            variant="default"
            className="rounded-full w-fit bg-primary-50 gap-2 items-center hidden md:flex"
            size="lg"
          >
            login
          </Button>
        </a>
      </div>
      {/* MOBILE NAV */}
      <Sheet>
        <SheetTrigger className="block md:hidden p-3">
          <span className="text-2xl text-slate-950 dark:text-slate-200">
            <Menu />
          </span>
        </SheetTrigger>

        <SheetContent>
          <SheetHeader>
            <a href="/">
              <img src={logo} className="cursor-pointer w-40 dark:invert" alt="" />
            </a>
            <SheetDescription>
              <div className="w-full space-y-3">
                <a href="/">
                  <Button variant="link" className="font-semibold text-md w-full">
                    Home
                  </Button>
                </a>
                <a href="/about">
                  <Button variant="link" className="font-semibold text-md w-full">
                    À propos
                  </Button>
                </a>
                <a href="/privacy-policy">
                  <Button variant="link" className="font-semibold text-md w-full">
                    Confidentialité
                  </Button>
                </a>
                <ModeToggle />
              </div>
            </SheetDescription>
          </SheetHeader>
        </SheetContent>
      </Sheet>
    </nav>
  );
};

export default Navbar;
