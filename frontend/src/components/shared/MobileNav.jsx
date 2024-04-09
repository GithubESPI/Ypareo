import { Sheet, SheetContent, SheetTrigger } from "../ui/sheet";
import menu from "/assets/icons/menu.svg";
import logo from "/assets/img/header/logo.png";
import NavItems from "./NavItems";
import { Separator } from "../ui/separator";

const MobileNav = () => {
  return (
    <nav className="md:hidden">
      <Sheet>
        <SheetTrigger className="align-middle">
          <img src={menu} alt="moblieNavMenu" width={24} height={24} className="cursor-pointer" />
        </SheetTrigger>
        <SheetContent className="flex flex-col gap-6 bg-white md:hidden">
          <img src={logo} alt="logo" width={128} height={38} />
          <Separator className="border border-gray-50" />
          <NavItems />
        </SheetContent>
      </Sheet>
    </nav>
  );
};

export default MobileNav;
