import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import FileUploader from "./FileUploader";

const formSchema = z.object({
  file: z.string().min(),
});

const EventForm = () => {
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      file: "",
    },
  });

  function onSubmit(values) {
    console.log(values);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col gap-5">
        <div className="flex flex-col justify-center md:flex-row">
          <FormField
            control={form.control}
            name="file"
            render={({ field }) => (
              <FormItem className="w-full">
                <FormControl className="h-72">
                  <FileUploader />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        <div className="flex gap-4  items-center justify-center">
          <Button
            type="submit"
            className="shad-button_primary"
          >
            Valider
          </Button>
        </div>
      </form>
    </Form>
  )
}

export default EventForm;
