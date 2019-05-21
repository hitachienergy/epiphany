FROM microsoft/dotnet:2.2-runtime AS base
WORKDIR /app

FROM microsoft/dotnet:2.2-sdk AS build
WORKDIR /src
COPY Epiphany.Examples.IoTHub.Connector.Console/Epiphany.Examples.IoTHub.Connector.Console.csproj Epiphany.Examples.IoTHub.Connector.Console/
COPY Messaging/Epiphany.Examples.Kafka/Epiphany.Examples.Kafka.csproj Messaging/Epiphany.Examples.Kafka/
COPY Messaging/Epiphany.Examples.Messaging/Epiphany.Examples.Messaging.csproj Messaging/Epiphany.Examples.Messaging/
RUN dotnet restore Epiphany.Examples.IoTHub.Connector.Console/Epiphany.Examples.IoTHub.Connector.Console.csproj
COPY . .
WORKDIR /src/Epiphany.Examples.IoTHub.Connector.Console
RUN dotnet build Epiphany.Examples.IoTHub.Connector.Console.csproj -c Release -o /app

FROM build AS publish
RUN dotnet publish Epiphany.Examples.IoTHub.Connector.Console.csproj -c Release -o /app

FROM base AS final
WORKDIR /app
COPY --from=publish /app .
ENTRYPOINT ["dotnet", "Epiphany.Examples.IoTHub.Connector.Console.dll"]
