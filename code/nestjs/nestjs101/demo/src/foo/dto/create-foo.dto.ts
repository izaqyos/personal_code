import { IsNotEmpty } from "class-validator";


export class CreateFooDTO {
    @IsNotEmpty()
    title: string;
}