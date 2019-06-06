FROM microsoft/dotnet:2.2-runtime AS base
WORKDIR /app

FROM microsoft/dotnet:2.2-sdk AS build
WORKDIR /src
COPY Epiphany.Examples.IoTHub.Metrics.Collector/Epiphany.Examples.IoTHub.Metrics.Collector.csproj Epiphany.Examples.IoTHub.Metrics.Collector/
COPY Messaging/Epiphany.Examples.Messaging/Epiphany.Examples.Messaging.csproj Messaging/Epiphany.Examples.Messaging/
RUN dotnet restore Epiphany.Examples.IoTHub.Metrics.Collector/Epiphany.Examples.IoTHub.Metrics.Collector.csproj
COPY . .
WORKDIR /src/Epiphany.Examples.IoTHub.Metrics.Collector
RUN dotnet build Epiphany.Examples.IoTHub.Metrics.Collector.csproj -c Release -o /app

FROM build AS publish
RUN dotnet publish Epiphany.Examples.IoTHub.Metrics.Collector.csproj -c Release -o /app

FROM base AS final
WORKDIR /app
COPY --from=publish /app .
ENTRYPOINT ["dotnet", "Epiphany.Examples.IoTHub.Metrics.Collector.dll"]
