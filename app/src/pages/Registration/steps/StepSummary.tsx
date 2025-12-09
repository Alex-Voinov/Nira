import type { IUser } from "@/types/user";


type Props = {
    data: IUser;
};

export default function StepSummary({ data }: Props) {
    return (
        <div className="step">
            <h2>Проверь свои данные</h2>
            <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
    );
}
