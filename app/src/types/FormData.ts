export type FormData = {
  name: string;
  age: number | null;
  gender: "male" | "female" | "other" | null;
  showGender: boolean;
  city: string;
  height: number | null;
  weight: number | null;
  interests: string[];
  about: string;
  tg_id?: number;
};