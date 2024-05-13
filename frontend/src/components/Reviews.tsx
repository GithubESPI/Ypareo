"use client";

import { useRef } from "react";
import MaxWidthWrapper from "./MaxWidthWrapper";

const ReviewGrid = () => {
  const containerRef = useRef<HTMLDivElement | null>(null);

  return (
    <div
      ref={containerRef}
      className="relative -mx-4 mt-16 grid h-[49rem max-h-[150px] grid-cols items-start gap-8 overflow-hidden px-4 sm:mt-20 md:grid-cols-2 lg:grid-cols-3"
    ></div>
  );
};

const Reviews = () => {
  return (
    <MaxWidthWrapper className="relative max-w-5xl">
      <ReviewGrid />
    </MaxWidthWrapper>
  );
};

export default Reviews;
