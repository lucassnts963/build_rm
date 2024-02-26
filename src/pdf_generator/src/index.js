import puppeteer from 'puppeteer'
import { load } from 'cheerio'
import fs from 'fs'
import { program } from 'commander'
import path from 'path'

program
    .option('-d, --dataPath <file>', 'Arquivo de dados JSON')
    .option('-o, --output <file>', 'Arquivo de saída PDF')
    .option('-n, --number <string>', 'Númeração da Requisição')
    .option('-de, --expedition <string>', 'Data de expedição')
    .option('-dr, --draw <string>', 'Identificação do desenho')
    .option('-tg, --tag <string>', 'Descrição do desenho')
    .option('-l, --local <string>', 'Local')
    .option('-dy, --destiny <string>', 'Destino')
    .option('-a, --aplication <string>', 'Aplicação')

program.parse(process.argv)

async function start () {
    const company = 'MONTISOL'
    
    try {
        const cwd = process.cwd()

        const { dataPath, output, number, expedition, draw, tag, local, destiny, aplication } = program.opts()

        if (!dataPath || !output || !number || !expedition || !draw || !tag || !local || !destiny || !aplication) {
            console.error('Por favor, informe todos os parâmentros.')
            return
        }

        const browser = await puppeteer.launch()
        const page = await browser.newPage()

        const templatePath = path.resolve(cwd, 'src', 'pdf_generator', 'src', 'template.html')
        const stylesPath = path.resolve(cwd, 'src', 'pdf_generator', 'src', 'styles.css')

        const htmlContent = fs.readFileSync(templatePath, 'utf-8')
        const jsonString = fs.readFileSync(dataPath, 'utf8')

        const jsonData = JSON.parse(jsonString)

        let $ = load(htmlContent)

        $('#company').text(company)
        $('#request_number').text(number)
        $('#contracted').text(company)
        $('#date').text(new Date().toUTCString())
        $('#expedition_date').text(expedition)
        $('#draw').text(draw)
        $('#tag').text(tag)
        $('#local').text(local)
        $('#destiny').text(destiny)
        $('#aplication').text(aplication)

        


        jsonData.forEach(item => {
            const tr = `
                <tr class="${ item.status }">
                    <td>${ item.code }</td>
                    <td>${ item.description }</td>
                    <td>${ item.dn }</td>
                    <td></td>
                    <td>${ item.quantity_requested }</td>
                    <td>${ item.quantity_required }</td>
                    <td>${ item.unit }</td>
                </tr>
            `

            $('#materials').append(tr)
        })



        const html = $.html()

        console.log(`Gerando PDF a partir de ${templatePath} para ${output}`)

        await page.setContent(html)
        await page.addStyleTag({ path: stylesPath })

        await page.pdf({ path: output, format: 'A4', landscape: true, preferCSSPageSize: true, printBackground: true })

        console.log(`PDF gerado com sucesso em ${output}`)

        await browser.close()
    } catch (error) {
        console.error('Ocorreu um erro:', error)
    }
}

start()
