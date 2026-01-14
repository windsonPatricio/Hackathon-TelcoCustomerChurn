# ===================================================================
# STAGE 1: Build (compila o JAR)
# ===================================================================
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

COPY .mvn .mvn
COPY mvnw pom.xml ./

# Torna o mvnw executável (garante permissão Linux)
RUN chmod +x mvnw

# Baixa dependências (Cache Layer)
RUN ./mvnw dependency:go-offline -B

# Copia o código fonte
COPY src ./src

# Build do JAR
RUN ./mvnw clean package -DskipTests

# ===================================================================
# STAGE 2: Runtime (executa a aplicação)
# ===================================================================
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Cria usuário não-root
RUN addgroup -S spring && adduser -S spring -G spring

# Copia o JAR do builder
COPY --from=builder /app/target/*.jar app.jar

# Define o usuário
USER spring:spring

EXPOSE 8080

# Entrypoint otimizado
ENTRYPOINT ["java", \
    "-XX:+UseContainerSupport", \
    "-XX:MaxRAMPercentage=75.0", \
    "-XX:InitialRAMPercentage=50.0", \
    "-XX:+UseG1GC", \
    "-Djava.security.egd=file:/dev/./urandom", \
    "-jar", \
    "app.jar"]