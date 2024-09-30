If you want to develop an email client in a language other than Python, there are several options that do not rely on `pip` or Python-based libraries. Arch Linux has excellent support for many programming languages, and you can develop the email client using one of them. Below are alternatives in different languages, each providing a way to interact with the Microsoft Graph API to send and receive emails.

### 1. **C++ (Using cURL or Boost)**

C++ is widely supported on Arch Linux, and you can use **cURL** or **Boost.Beast** for HTTP requests to the Microsoft Graph API.

#### Install Dependencies

```bash
sudo pacman -S gcc curl cmake boost
```

#### Example (Using cURL for HTTP Requests)

```cpp
#include <iostream>
#include <curl/curl.h>

const std::string GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0";

std::string send_email(const std::string& access_token, const std::string& recipient, const std::string& subject, const std::string& body) {
    CURL* curl;
    CURLcode res;
    struct curl_slist* headers = nullptr;

    curl = curl_easy_init();
    if (curl) {
        std::string url = GRAPH_API_ENDPOINT + "/me/sendMail";
        std::string json_payload = R"(
            {
                "message": {
                    "subject": ")" + subject + R"(",
                    "body": {
                        "contentType": "Text",
                        "content": ")" + body + R"("
                    },
                    "toRecipients": [
                        {"emailAddress": {"address": ")" + recipient + R"("}}
                    ]
                },
                "saveToSentItems": "true"
            }
        )";

        headers = curl_slist_append(headers, ("Authorization: Bearer " + access_token).c_str());
        headers = curl_slist_append(headers, "Content-Type: application/json");

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_payload.c_str());

        res = curl_easy_perform(curl);

        if (res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

        curl_easy_cleanup(curl);
        return (res == CURLE_OK) ? "Email sent successfully!" : "Failed to send email";
    }
    return "Initialization failed";
}

int main() {
    std::string access_token = "your_access_token_here";
    std::string recipient = "recipient@example.com";
    std::string subject = "Test Email";
    std::string body = "This is a test email from C++ client!";
    std::cout << send_email(access_token, recipient, subject, body) << std::endl;
    return 0;
}
```

- **OAuth**: You'll need to handle OAuth2 authentication either using another library or calling a shell script that uses `curl` to retrieve the access token.
- You can replace `cURL` with **Boost.Beast** for modern C++ HTTP requests if you prefer.

### 2. **C# (Using .NET Core)**

C# with .NET Core is cross-platform and works well on Arch Linux. You can easily interact with Microsoft services using the **Microsoft Graph SDK**.

#### Install .NET SDK

```bash
sudo pacman -S dotnet-sdk
```

#### Example (Using Microsoft Graph SDK)

```bash
dotnet new console -n EmailClient
cd EmailClient
dotnet add package Microsoft.Graph
dotnet add package Microsoft.Identity.Client
```

#### Program.cs

```csharp
using Microsoft.Graph;
using Microsoft.Identity.Client;
using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    private static async Task<string> GetAccessToken()
    {
        var clientApp = ConfidentialClientApplicationBuilder.Create("your-client-id")
            .WithClientSecret("your-client-secret")
            .WithAuthority(new Uri("https://login.microsoftonline.com/your-tenant-id"))
            .Build();

        var result = await clientApp.AcquireTokenForClient(new[] { "https://graph.microsoft.com/.default" }).ExecuteAsync();
        return result.AccessToken;
    }

    private static async Task SendEmail(GraphServiceClient graphClient)
    {
        var message = new Message
        {
            Subject = "Test Email",
            Body = new ItemBody
            {
                ContentType = BodyType.Text,
                Content = "This is a test email from C# client on Arch Linux!"
            },
            ToRecipients = new Recipient[]
            {
                new Recipient
                {
                    EmailAddress = new EmailAddress
                    {
                        Address = "recipient@example.com"
                    }
                }
            }
        };

        await graphClient.Me.SendMail(message, true).Request().PostAsync();
        Console.WriteLine("Email sent successfully!");
    }

    static async Task Main(string[] args)
    {
        var accessToken = await GetAccessToken();
        var graphClient = new GraphServiceClient(new DelegateAuthenticationProvider(
            async (requestMessage) =>
            {
                requestMessage.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", accessToken);
            }));

        await SendEmail(graphClient);
    }
}
```

Run the application:

```bash
dotnet run
```

### 3. **Go (Using HTTP and OAuth Libraries)**

Go is another excellent choice for building an email client, and it runs well on Arch Linux. Go's standard library includes great support for HTTP requests, and you can handle OAuth2 using third-party libraries.

#### Install Go

```bash
sudo pacman -S go
```

#### Example

1. Install the necessary libraries:

```bash
go get golang.org/x/oauth2
go get google.golang.org/api/option
```

2. Write your Go code:

```go
package main

import (
    "bytes"
    "fmt"
    "net/http"
    "io/ioutil"
)

const GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

func sendEmail(accessToken, recipient, subject, body string) error {
    url := GRAPH_API_ENDPOINT + "/me/sendMail"
    emailPayload := fmt.Sprintf(`{
        "message": {
            "subject": "%s",
            "body": {
                "contentType": "Text",
                "content": "%s"
            },
            "toRecipients": [
                {"emailAddress": {"address": "%s"}}
            ]
        },
        "saveToSentItems": "true"
    }`, subject, body, recipient)

    req, err := http.NewRequest("POST", url, bytes.NewBuffer([]byte(emailPayload)))
    if err != nil {
        return err
    }
    req.Header.Set("Authorization", "Bearer "+accessToken)
    req.Header.Set("Content-Type", "application/json")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    bodyBytes, _ := ioutil.ReadAll(resp.Body)
    fmt.Println("Response: ", string(bodyBytes))

    return nil
}

func main() {
    accessToken := "your_access_token_here"
    recipient := "recipient@example.com"
    subject := "Test Email from Go"
    body := "This is a test email from Go client on Arch Linux!"
    err := sendEmail(accessToken, recipient, subject, body)
    if err != nil {
        fmt.Println("Failed to send email:", err)
    }
}
```

#### Run the Go Client

```bash
go run main.go
```

### 4. **Rust (Using Reqwest for HTTP)**

Rust is known for its speed and safety and is well-supported on Arch Linux. You can use **Reqwest** for HTTP requests to the Microsoft Graph API.

#### Install Rust

```bash
sudo pacman -S rust
```

#### Example (Using Reqwest)

1. Create a new Rust project:

```bash
cargo new email_client
cd email_client
```

2. Add dependencies to `Cargo.toml`:

```toml
[dependencies]
reqwest = { version = "0.11", features = ["json"] }
tokio = { version = "1", features = ["full"] }
```

3. Write the code (`src/main.rs`):

```rust
use reqwest::Client;
use std::error::Error;

const GRAPH_API_ENDPOINT: &str = "https://graph.microsoft.com/v1.0";

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let access_token = "your_access_token_here";
    let recipient = "recipient@example.com";
    let subject = "Test Email from Rust";
    let body = "This is a test email from Rust client on Arch Linux!";

    let client = Client::new();
    let url = format!("{}/me/sendMail", GRAPH_API_ENDPOINT);
    let payload = serde_json::json!({
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                { "emailAddress": { "address": recipient } }
            ]
        },
        "saveToSentItems": "true"
    });

    let response = client.post(&url)
        .bearer_auth(access_token)
        .json(&payload)
        .send()
        .await?;

    println!("Response: {:?}", response);
    Ok(())
}
```

4. Run the application:

```bash
cargo run
```

---

### Summary

Each language (C++, C#, Go, and Rust) provides a
