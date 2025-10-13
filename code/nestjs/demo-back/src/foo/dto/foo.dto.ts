import { IsNotEmpty } from "class-validator";

export class FooDTO {
    @IsNotEmpty()
    title: string;
}