import { headerLinks } from "@/constants";

const NavItems = () => {
  return (
    <ul className="md:flex-between flex w-full flex-col items-start gap-5 md:flex-row">
      {headerLinks.map((link) => {
        const isActive = link.route;

        return (
          <li key={link.route} className={`${isActive} flex-center p-medium-16 whitespace-nowrap`}>
            <a href={link.route}>{link.label}</a>
          </li>
        );
      })}
    </ul>
  );
};

export default NavItems;
