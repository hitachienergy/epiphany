FROM microsoft/dotnet:2.2-runtime AS base
WORKDIR /app

FROM microsoft/dotnet:2.2-sdk AS build
WORKDIR /src
COPY Epiphany.Examples.Messaging.Console/Epiphany.Examples.Messaging.Console.csproj Epiphany.Examples.Messaging.Console/
COPY Messaging/Epiphany.Examples.Kafka/Epiphany.Examples.Kafka.csproj Messaging/Epiphany.Examples.Kafka/
COPY Messaging/Epiphany.Examples.Messaging/Epiphany.Examples.Messaging.csproj Messaging/Epiphany.Examples.Messaging/
COPY Messaging/Epiphany.Examples.RabbitMQ/Epiphany.Examples.RabbitMQ.csproj Messaging/Epiphany.Examples.RabbitMQ/
RUN dotnet restore Epiphany.Examples.Messaging.Console/Epiphany.Examples.Messaging.Console.csproj
COPY . .
WORKDIR /src/Epiphany.Examples.Messaging.Console
RUN dotnet build Epiphany.Examples.Messaging.Console.csproj -c Release -o /app

FROM build AS publish
RUN dotnet publish Epiphany.Examples.Messaging.Console.csproj -c Release -o /app

FROM base AS final
WORKDIR /app
COPY --from=publish /app .
ENTRYPOINT ["dotnet", "Epiphany.Examples.Messaging.Console.dll"]
