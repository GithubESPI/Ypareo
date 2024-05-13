import { cn } from "@/lib/utils";
import Image from "next/image";
import { HTMLAttributes } from "react";

interface ExcelProps extends HTMLAttributes<HTMLDivElement> {
  imgSrc: string;
  dark?: boolean;
}

const Excel = ({ imgSrc, className, dark = false, ...props }: ExcelProps) => {
  return (
    <div className={cn("relative pointer-events-none z-50 overflow-hidden", className)} {...props}>
      <Image
        src={dark ? "/darkexcel.png" : "/darkexcel.png"}
        className="pointer-events-none z-50 select-none"
        alt="darkexcel"
        width={956}
        height={956}
      />

      {/* <div className="absolute -z-10 inset-0">
        <Image
          className="object-cover"
          src={imgSrc}
          alt="overlaying phone image"
          width={256}
          height={256}
        />
      </div> */}
    </div>
  );
};

export default Excel;
