export type FormData = {
  tg_id: number;
  name: string;
  age: number;
  gender: "male" | "female" | "other" | null;
  showGender: "male" | "female" | "mix" | null;
  city: string;
  current_country: string | null;
  height: number | null;
  weight: number | null;
  goal: string[];
  description: string | null;
};

export const formInitialState: FormData = {
  name: "",
  age: -1,
  gender: null,
  showGender: null,
  city: "",
  current_country: null,
  height: null,
  weight: null,
  goal: [],
  description: "",
  tg_id: -1,
};