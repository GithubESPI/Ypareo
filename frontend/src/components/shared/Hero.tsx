const Hero = () => {
  return (
    <div className="space-y-16 pb-8">
      {/* Title + Desc */}
      <div className="space-y-6">
        <h1 className="text-3xl md:text-5xl font-medium text-center">Convertisseur de bulletin</h1>
        <p className="text-muted-foreground text-md md:text-lg text-center md:px-24 xl:px-44 2xl:px-52">
          Charger vos fichiers Excel contenant les données scolaires et génèrer automatiquement vos
          bulletins semestriels au format Word.
        </p>
      </div>
    </div>
  );
};

export default Hero;
