import userService from "@/services/userService";
import type { IUser } from "@/types/user";


type Props = {
    data: IUser;
};

export default function StepSummary({ data }: Props) {
    const saveData = () => {
        userService.register(data).then(response => {
            if (!response.ok) throw new Error("Ошибка сохранения");
            alert("Данные успешно сохранены!");
        }).catch(err => {
            console.error(err);
            alert("Не удалось сохранить данные. Попробуй еще раз.");
        }
        )
    };

    return (
        <div className="step">
            <h2>Проверь свои данные</h2>
            <pre>{JSON.stringify(data, null, 2)}</pre>
            <button onClick={saveData} className="btn-save">
                Сохранить
            </button>
        </div>
    );
}
