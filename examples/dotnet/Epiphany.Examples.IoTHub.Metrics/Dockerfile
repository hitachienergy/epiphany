FROM microsoft/dotnet:2.2-runtime AS base
WORKDIR /app

FROM microsoft/dotnet:2.2-sdk AS build
WORKDIR /src
COPY Epiphany.Examples.IoTHub.Metrics/Epiphany.Examples.IoTHub.Metrics.csproj Epiphany.Examples.IoTHub.Metrics/
RUN dotnet restore Epiphany.Examples.IoTHub.Metrics/Epiphany.Examples.IoTHub.Metrics.csproj
COPY . .
WORKDIR /src/Epiphany.Examples.IoTHub.Metrics
RUN dotnet build Epiphany.Examples.IoTHub.Metrics.csproj -c Release -o /app

FROM build AS publish
RUN dotnet publish Epiphany.Examples.IoTHub.Metrics.csproj -c Release -o /app

FROM base AS final
WORKDIR /app
COPY --from=publish /app .
ENTRYPOINT ["dotnet", "Epiphany.Examples.IoTHub.Metrics.dll"]
