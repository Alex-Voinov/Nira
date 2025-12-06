import type { FormData } from "@/types/FormData";
const API_URL = import.meta.env.VITE_API_URL;

type Props = {
    data: FormData;
};

export default function StepSummary({ data }: Props) {
    const saveData = async () => {
        try {
            const response = await fetch(`${API_URL}/registration`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });
            if (!response.ok) throw new Error("Ошибка сохранения");
            alert("Данные успешно сохранены!");
        } catch (err) {
            console.error(err);
            alert("Не удалось сохранить данные. Попробуй еще раз.");
        }
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
