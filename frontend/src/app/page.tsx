import Excel from "@/components/Excel";
import { Icons } from "@/components/Icons";
import MaxWidthWrapper from "@/components/MaxWidthWrapper";
import Reviews from "@/components/Reviews";
import { Check } from "lucide-react";

const page = () => {
  return (
    <div className="bg-slate-50">
      <section>
        <MaxWidthWrapper className="pb-24 pt-10 lg:grid lg:grid-cols-3 sm:pb-32 lg:gap-x-0 xl:gap-x-8 lg:pt-24 xl:pt-32 lg:pb-52">
          <div className="col-span-2 px-6 lg:px-0 lg:pt-4">
            <div className="relative mx-auto text-center lg:text-left flex flex-col items-center lg:items-start">
              {/* <div className="absolute w-28 left-0 -top-20 hidden lg:block">
                <Image src="/logo.png" alt="logo" width={200} height={200} />
              </div> */}
              <h1 className="relative w-fit tracking-tight text-balance mt-16 font-bold !leading-tight text-gray-900 text-5xl md:text-6xl lg:text-7xl">
                Convertir des tableaux <span className="bg-primary-50 px-2 text-white">excels</span>{" "}
                en bulletins de notes
              </h1>
              <p className="mt-8 text-lg lg:pr-10 max-w-prose text-center lg:text-left text-balance md:text-wrap">
                Charger vos fichiers excels contenant les données scolaires et génèrer
                <span className="font-semibold"> automatiquement</span> vos bulletins semestriels et
                annuels au format Word.
              </p>

              <ul className="mt-8 space-y-2 text-left font-medium flex flex-col items-center sm:items-start">
                <div className="space-y-2">
                  <li className="flex gap-1.5 items-center text-left">
                    <Check className="h-5 w-5 shrink-0 text-primary-50" />
                    Haute qualité des bulletins
                  </li>
                  <li className="flex gap-1.5 items-center text-left">
                    <Check className="h-5 w-5 shrink-0 text-primary-50" />
                    Calculs des notes et des coefficients
                  </li>
                  <li className="flex gap-1.5 items-center text-left">
                    <Check className="h-5 w-5 shrink-0 text-primary-50" />
                    Choix entre bulletins semestriels et annuels
                  </li>
                </div>
              </ul>
            </div>
          </div>

          <div className="col-span-full lg:col-span-1 w-full flex justify-center px-8 sm:px-16 md:px-0 mt-32 lg:mx-0 lg:mt-20 h-fit">
            <div className="relative md:max-w-xl">
              <Excel className="w-96" imgSrc="/excel.png" />
            </div>
          </div>
        </MaxWidthWrapper>
      </section>

      {/* value proposition section*/}
      <section className="bg-slate-100 py-24">
        <MaxWidthWrapper className="flex flex-col items-center gap-4 sm:gap-32">
          <div className="flex flex-col lg:flex-row items-center gap-4 sm:gap-6">
            <h2 className="order-1 mt-2 tracking-tight text-center text-balance !leading-tight font-bold text-5xl md:text-6xl text-gray-900">
              Une utilisation{" "}
              <span className="relative px-2">
                rapide{" "}
                <Icons.underline className="hidden sm:block pointer-events-none absolute inset-x-0 -bottom-6 text-primary-50" />
              </span>{" "}
              et efficace
            </h2>
          </div>

          <div className="mx-auto grid max-w-2xl grid-cols-1 px-4 lg:mx-0 lg:max-w-none lg:grid-cols-2 gap-y-16">
            <div className="flex flex-auto flex-col gap-4 lg:pr-8 xl:pr-20">
              <div className="flex gap-0.5 mb-2">
                <div className="text-lg leading-8">
                  <p>
                    Glisser ou déposer un fichier excel contenant les notes, les coefficents, les
                    noms et prénoms des apprenants. Ces fichiers excels seront
                    <span className="p-0.5 bg-slate-800 text-white"> les relevés de notes</span> des
                    apprenants selon leurs classes.
                  </p>
                </div>
              </div>
            </div>

            <div className="flex flex-auto flex-col gap-4 lg:pr-8 xl:pr-20">
              <div className="flex gap-0.5 mb-2">
                <div className="text-lg leading-8">
                  <p>
                    Une fois que le document excel est déposé et uploadé, vous pourrez cliquer sur
                    le bouton{" "}
                    <span className="p-0.5 bg-slate-800 text-white">Générer les bulletins</span>{" "}
                    pour avoir les bulletins semestriels ou annuels de chaques apprenants.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </MaxWidthWrapper>

        <div className="pt-16">
          <Reviews />
        </div>
      </section>
    </div>
  );
};

export default page;
