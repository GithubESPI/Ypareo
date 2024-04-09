import Header from "@/components/shared/Header";

const RootLayout = ({ children }) => {
  return (
    <div>
      <Header />
      {children}
    </div>
  );
};

export default RootLayout;
