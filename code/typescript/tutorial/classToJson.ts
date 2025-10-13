class example{
    private a: string;
    private b: string;
    private c?: string = ' with optional member';

    public constructor(a: string,b: string, c?: string) {
        this.a = a;
        this.b = b;
        this.c = c;
    }
}

let ex: example = new example('class', ' to json');
console.log(JSON.stringify(ex, null, 4));

let ex1: example = new example('class', ' to json', ' set optional');
console.log(JSON.stringify(ex1, null, 4));

interface data {

    a: string;
    b?: string;
}

const dt: data = {
    'a': 'aaa'
};
console.log(JSON.stringify(dt, null, 4));


const dt1: data = {
    'a': 'aaa1',
    'b': 'bbb'
};
console.log(JSON.stringify(dt1, null, 4));

