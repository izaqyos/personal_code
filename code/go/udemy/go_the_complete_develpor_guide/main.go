package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

type logWriter struct{}

func main() {

	resp, err := http.Get("http://google.com")
	if err != nil {
		fmt.Println("Got err,", err)
		os.Exit(1)

	} else {
		// ver 1. note, no body:
		// fmt.Println(resp)
		// Got response &{200 OK 200 HTTP/1.1 1 1 map[Cache-Control:[private, max-age=0] Content-Type:[text/html; charset=ISO-8859-1] Date:[Thu, 25 Feb 2021 11:48:37 GMT] Expires:[-1] P3p:[CP="This is not a P3P policy! See g.co/p3phelp for more info."] Server:[gws] Set-Cookie:[1P_JAR=2021-02-25-11; expires=Sat, 27-Mar-2021 11:48:37 GMT; path=/; domain=.google.com; Secure NID=210=s7ngk-NcrCoN1O_JSwHpIo9SH2yI0jPbN8uQKldy42U_N6NAzAnJeCHXhUSQPtnctSysGMYLI60bq_-5s_C4TUFfMFBd1dOvy4o9uyjwu8lW4wo1QQEpHhu9BSalBPt98tde_-sNwLrERKJzLkwZIciuOYqYPYCrZYxt-yDjl3g; expires=Fri, 27-Aug-2021 11:48:36 GMT; path=/; domain=.google.com; HttpOnly] X-Frame-Options:[SAMEORIGIN] X-Xss-Protection:[0]] 0xc00000e0e0 -1 [] false true map[] 0xc0000f2100 <nil>}

		// // ver 2. read directly from resp.Body reader
		// respData := make([]byte, (int)(math.Pow(10, 5)))
		// resp.Body.Read(respData)
		// fmt.Println(string(respData))

		// ver 3. use redirct resp.Body reader into stdout
		// io.Copy(os.Stdout, resp.Body)

		logger := logWriter{}
		// ver 4. dumb writer, like > /dev/null
		//io.Copy(logger, resp.Body)

		//ver 5, correct Writer impl
		io.Copy(logger, resp.Body)
	}
}

//logWriter now implements io.Writer interface
func (logWriter) Write(bs []byte) (int, error) {
	// ver 4 dumb code, demo breaking interface
	// return 1, nil
	fmt.Println(string(bs))
	fmt.Println("Wrote", len(bs), "bytes")
	return len(bs), nil

}
