import type { IUser } from "@/types/user";

type Props = {
  data: IUser;
  setData: (data: IUser) => void;
};

export default function StepAbout({ data, setData }: Props) {
  return (
    <div className="step">
      <h2>О себе</h2>
      <textarea
        value={data.description || ''}
        onChange={(e) => setData({ ...data, description: e.target.value })}
        placeholder="Расскажи немного о себе"
        className="textarea"
        rows={4}
      />
    </div>
  );
}
